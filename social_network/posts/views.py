import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from posts import models, forms


# Create your views here.
@login_required
def delete_post(request, post_pk):
    post = models.Posts.objects.post(post_pk)
    if request.user == post.user or request.user == post.to_user:
        post.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    raise Http404('Это не ваш пост')


@login_required
def delete_comment(request, comment_pk):
    comment = models.Comments.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    raise Http404('Это не ваш комментарий')


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = models.Posts
    form_class = forms.PostForm
    template_name = 'posts/update_post.html'
    extra_context = {'title': 'Редактирование записи'}
    pk_url_kwarg = 'post_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prev_url = self.request.META.get('HTTP_REFERER')
        if prev_url:
            self.request.session['prev_url'] = prev_url
        return context

    def get_object(self, queryset=None):
        post = models.Posts.objects.post(self.kwargs['post_pk'])
        if self.request.user == post.user:
            return post
        raise Http404('Данный пост вам не принадлежит')

    def form_valid(self, form):
        post = models.Posts.objects.post(self.kwargs['post_pk'])
        form = form.save(commit=False)
        form.user = post.user
        form.to_user = post.to_user
        form.profile = post.profile
        form.date_modified = datetime.datetime.now()
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        if 'prev_url' in self.request.session:
            return self.request.session['prev_url']
        return reverse_lazy('core:profile', kwargs={'profile_slug': self.request.user.profile.slug})
