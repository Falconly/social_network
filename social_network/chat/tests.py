from django.test import TestCase
from django.urls import reverse

from core.tests import BaseTest
from chat import models, services


# Create your tests here.
class ChatTest(BaseTest, TestCase):
    def test_create_chat(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('chat:create_chat', kwargs={'user_id': self.user2.pk}))

        self.assertEqual(response.status_code, 302)
        services.get_chats(self.user.pk, self.user2.pk)





