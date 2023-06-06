from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from chat import models, forms, services


# Create your views here.


class ShowMessagesView(LoginRequiredMixin, FormMixin, ListView):
    model = models.Messages
    template_name = 'chat/chat.html'
    form_class = forms.MessageForm

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.chat = get_object_or_404(models.Chat, pk=self.kwargs['chat_pk'])
        self.to_user = services.get_to_user(self.chat, self.request.user.pk)
        self.messages = services.get_messages_list(self.request.user, self.to_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = {'title': 'Личные сообщения', 'messages': self.messages, 'to_user': self.to_user,
                 'chat_pk': self.chat.pk}
        context.update(c_def)
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        form = form.save(commit=False)
        form.from_user = self.request.user
        form.to_user = self.to_user
        form.chat_id = self.kwargs['chat_pk']
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('chat:messages', kwargs={'chat_pk': self.kwargs['chat_pk']})


class CreateChatView(View):
    def get(self, request, user_id):
        chats = services.get_chats(request.user.pk, user_id)
        if chats.count() == 0:
            user = services.get_user(user_id)
            chat = services.create_chat()
            chat.members.add(request.user)
            chat.members.add(user)
        else:
            chat = chats.first()
        return redirect(reverse('chat:messages', kwargs={'chat_pk': chat.pk}))


class ListChatView(ListView):
    model = models.Chat
    template_name = 'chat/list_chat.html'
    context_object_name = 'users'
    extra_context = {'title': 'Список чатов'}

    def get_queryset(self):
        qs = services.get_user_chat(self.request.user)
        return qs
