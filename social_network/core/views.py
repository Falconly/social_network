from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.views.generic.edit import FormMixin

from friendship.models import Friend, Block, FriendshipRequest

from core import forms
from core import models
from core import services

from posts.forms import PostForm, CommentForm
from posts.models import Posts


# Create your views here.
class RegisterUserView(CreateView):
    form_class = forms.RegisterUserForm
    template_name = 'core/Auth/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('core:profile', profile_slug=user.profile.slug)


class LoginUserView(LoginView):
    template_name = 'core/Auth/login.html'
    form_class = forms.LoginUserForm
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse('core:profile', kwargs={'profile_slug': self.request.user.profile.slug})


class ShowNewsView(LoginRequiredMixin, FormMixin, ListView):
    model = Posts
    template_name = 'core/Network/news.html'
    context_object_name = 'posts'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('core:news')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': 'Новостная лента'}
        context.update(c_def)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        form = form.save(commit=False)
        post_id = int(self.request.POST.get('id'))

        form.user = self.request.user
        form.profile = self.request.user.profile
        form.post = Posts.objects.post(post_id)
        form.save()

        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, FormMixin, DetailView):
    model = models.Profile
    template_name = None
    slug_url_kwarg = 'profile_slug'
    context_object_name = 'user'
    form_class = PostForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.other_user = services.get_other_profile(self.kwargs['profile_slug'])
        self.user = self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.user.profile.slug

        if self.request.POST and 'id' in self.request.POST:
            context['comment_form'] = CommentForm(self.request.POST)
        else:
            context['comment_form'] = CommentForm()

        if self.template_name == 'core/Network/profile/profile.html':
            posts = Posts.objects.posts(self.user)

            c_def = {'title': f'{self.user.first_name} {self.user.last_name}', 'profile': self.user.profile,
                     'slug': slug, 'posts': posts}
        else:
            posts = Posts.objects.posts(self.other_user.user)
            reverse_request = services.get_reverse_friend_request(self.user, self.other_user.user)
            if reverse_request:
                if reverse_request.rejected:
                    context.update({'reject': True})
                else:
                    context.update({'reverse_request': True})
            else:
                friend_request = services.get_friend_request(self.user, self.other_user.user)
                if friend_request:
                    if friend_request.rejected:
                        context.update({'request_rejected': True})
                    else:
                        context.update({'friend_request': True})
                else:
                    if services.check_are_friends(self.user, self.other_user.user):
                        context.update({'are_friends': True})
            c_def = {'title': f'{self.other_user.user.first_name} {self.other_user.user.last_name}',
                     'profile': self.other_user, 'slug': slug, 'posts': posts}
        context.update(c_def)
        return context

    def get_object(self, queryset=None):
        if self.other_user.user.pk == self.user.pk:
            self.template_name = 'core/Network/profile/profile.html'
        else:
            self.template_name = 'core/Network/profile/other_profile.html'
        return self.user

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        form = self.get_form()
        if context['form'].is_valid():
            return self.form_valid(form)

        elif context['comment_form'].is_valid():
            form = context['comment_form']
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        context = self.get_context_data()
        form = form.save(commit=False)
        form.user = self.user
        form.profile = self.user.profile

        if context['comment_form'].is_valid():
            post_id = int(self.request.POST.get('id'))
            form.post = Posts.objects.post(post_id)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('core:profile', kwargs={'profile_slug': self.kwargs['profile_slug']})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    form_class = forms.UpdateProfileForm
    template_name = 'core/Network/profile/update_profile.html'
    slug_url_kwarg = 'profile_slug'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': f"Редактирование профиля - {self.request.user.username}"}
        if self.request.POST:
            context['user_form'] = forms.UpdateUserForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = forms.UpdateUserForm(instance=self.request.user)
        context.update(c_def)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(UpdateProfileView, self).form_valid(form)


class PeoplesListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'core/Network/peoples.html'
    context_object_name = 'users'
    extra_context = {'title': 'Люди'}


@login_required
def friendship_request(request, profile_slug: str):
    other_user = services.get_other_profile(profile_slug).user
    qs = services.get_reverse_friend_request(request.user, other_user)
    if qs:
        qs.cancel()
    services.get_add_friend(request.user, other_user)
    return redirect('core:profile', profile_slug)


@login_required
def friend_request_accept(request, profile_slug: str):
    other_user = services.get_other_profile(profile_slug).user

    user = request.user
    friend_request = services.get_reverse_friend_request(user, other_user)
    if friend_request:
        friend_request.accept()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def friend_request_reject(request, profile_slug: str):
    other_user = services.get_other_profile(profile_slug).user
    user = request.user
    friend_request = services.get_reverse_friend_request(user, other_user)
    if friend_request:
        friend_request.reject()
    return redirect(request.META.get('HTTP_REFERER'))


class ShowFriendsView(LoginRequiredMixin, ListView):
    model = Friend
    template_name = 'core/Network/friends/friends.html'
    context_object_name = 'friends'

    def get_queryset(self):
        list_friend = services.get_list_friends(self.request.user)
        return list_friend

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': 'Друзья'}
        context.update(c_def)
        return context


class ShowSubsView(LoginRequiredMixin, ListView):
    model = models.Profile
    template_name = 'core/Network/friends/subs.html'
    extra_context = {'title': 'Заявки'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_requests = services.get_list_friend_request_input(self.request.user)
        c_def = {'title': 'Заявки', 'friend_requests': friend_requests}
        context.update(c_def)
        return context


@login_required
def delete_friend(request, friend_slug: str):
    other_user = services.get_other_profile(friend_slug).user
    user = request.user
    services.get_remove_friend(user, other_user)
    return redirect(request.META.get('HTTP_REFERER'))


class ShowFromRequestView(LoginRequiredMixin, ListView):
    model = FriendshipRequest
    template_name = "core/Network/friends/from_request.html"
    extra_context = {'title': 'Отправленные заявки', 'h': 'Список отправленных заявок'}
    context_object_name = 'friend_requests'

    def get_queryset(self):
        friend_requests = services.get_sent_requests(self.request.user)
        return friend_requests


class ShowRejectedRequestsView(LoginRequiredMixin, ListView):
    model = FriendshipRequest
    template_name = 'core/Network/friends/rejected_requests.html'
    context_object_name = 'rejected_requests'
    extra_context = {'title': 'Отклоненные заявки'}

    def get_queryset(self):
        rejected_requests = FriendshipRequest.objects.select_related('from_user').filter(from_user=self.request.user)
        return rejected_requests


class ShowYouRejectedRequestsView(LoginRequiredMixin, ListView):
    model = Friend
    template_name = 'core/Network/friends/your_rejected_requests.html'
    context_object_name = 'rejected_requests'
    extra_context = {'title': 'Вами отклоненные заявки'}

    def get_queryset(self):
        rejected_request = Friend.objects.rejected_requests(user=self.request.user)
        return rejected_request


@login_required
def friendship_request_delete(request, other_slug: str):
    other_user = services.get_other_profile(other_slug).user
    user = request.user
    friend_request = services.get_friend_request(user, other_user)
    if friend_request:
        friend_request.cancel()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def friendship_request_repeat(request, other_slug: str):
    other_user = services.get_other_profile(other_slug).user
    user = request.user
    friend_request = services.get_friend_request(user, other_user)
    if friend_request:
        friend_request.cancel()
        services.get_add_friend(request.user, other_user)
    return redirect('core:from_request', user.profile.slug)


@login_required
def block_user(request, other_slug: str):
    other_user = services.get_other_profile(other_slug).user
    services.get_block_user(request.user, other_user)
    return redirect(request.META.get('HTTP_REFERER'))


class ShowBlockedUsersView(LoginRequiredMixin, ListView):
    model = Block
    template_name = 'core/Network/friends/blocked_users.html'
    context_object_name = 'blocked_users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {'title': 'Заблокированные пользователи'}
        context.update(c_def)
        return context

    def get_queryset(self):
        return services.get_blocked_users(self.request.user)


@login_required
def remove_block(request, other_slug: str):
    other_user = services.get_other_profile(other_slug).user
    services.get_remove_block(request.user, other_user)
    return redirect(request.META.get('HTTP_REFERER'))
