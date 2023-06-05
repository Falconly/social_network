from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from core import services


# Create your tests here.
class BaseTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        user_data = {
            'first_name': 'Name',
            'last_name': 'last_name',
            'username': 'Login2',
            'email': 'anfjasbn@mail.ru',
            'password': 'er2jiuwhuichwt'
        }
        self.user = get_user_model().objects.create_user(**user_data)
        user2_data = {
            'first_name': 'Name',
            'last_name': 'last_name',
            'username': 'Login10',
            'email': 'anfjasbn@mail.ru',
            'password': 'er2jiuwhuichwt'
        }
        self.user2 = get_user_model().objects.create(**user2_data)


class AuthTest(BaseTest, TestCase):
    def test_register_user_valid_data(self):
        form_data = {
            'first_name': 'Name',
            'last_name': 'last_name',
            'username': 'LoginP',
            'email': 'anfjasbn@mail.ru',
            'password1': 'er2jiuwhuichwt',
            'password2': 'er2jiuwhuichwt'
        }

        response = self.client.post(reverse('core:register'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(response.context['user'].profile)

    def test_register_user_short_password(self):
        form_data = {
            'first_name': 'Name',
            'last_name': 'last_name',
            'username': 'Login3',
            'email': 'anfjasbn@mail.ru',
            'password1': 'ert',
            'password2': 'ert'
        }

        response = self.client.post(reverse('core:register'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_register_user_invalid_email(self):
        form_data = {
            'first_name': 'Name',
            'last_name': 'last_name',
            'username': 'Login4',
            'email': 'anfjasbnmail.ru',
            'password1': 'er2jiuwhuichwt',
            'password2': 'er2jiuwhuichwt'
        }

        response = self.client.post(reverse('core:register'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/Auth/register.html')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_register_user_none_fname_lname(self):
        form_data = {
            'first_name': '',
            'last_name': '',
            'username': 'Login4',
            'email': 'anfjasbn@mail.ru',
            'password1': 'er2jiuwhuichwt',
            'password2': 'er2jiuwhuichwt'
        }

        response = self.client.post(reverse('core:register'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/Auth/register.html')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_login_user(self):
        form_data = {
            'username': 'Login2',
            'password': 'er2jiuwhuichwt'
        }

        response = self.client.post(reverse('core:home'), data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)


class ProfileTest(BaseTest, TestCase):
    def test_detail_view_profile(self):
        self.client.login(username='Login2', password='er2jiuwhuichwt')
        response = self.client.get(reverse('core:profile', kwargs={'profile_slug': self.user.profile.slug}),
                                   follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/Network/profile/profile.html')

    def test_not_auth_detail_view_profile(self):
        self.client.login(username='Login2', password='er2jiuwhuichwt')
        response = self.client.get(reverse('core:profile', kwargs={'profile_slug': self.user2.profile.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/Network/profile/other_profile.html')

    def test_update_view_profile(self):
        self.client.login(username='Login2', password='er2jiuwhuichwt')
        form_data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'slug': 'ivan',
            'bio': 'Биография',
            'date_birthday': '24.09.2012'

        }
        response = self.client.post(reverse('core:update_profile', kwargs={'profile_slug': self.user.profile.slug}),
                                    data=form_data)

        self.assertEqual(response.status_code, 302)

    def test_update_view_profile_invalid(self):
        self.client.login(username='Login2', password='er2jiuwhuichwt')
        form_data = {
            'first_name': '',
            'last_name': '',
            'slug': 'ivan',
            'bio': 'Биография',
            'date_birthday': '24.09.2012'

        }
        response = self.client.post(reverse('core:update_profile', kwargs={'profile_slug': self.user.profile.slug}),
                                    data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertNotEquals(response.context['user'].first_name, form_data['first_name'])
        self.assertNotEquals(response.context['user'].last_name, form_data['last_name'])


class FriendShipRequestTest(BaseTest, TestCase):
    def test_friend_request(self):
        self.client.login(username='Login2', password='er2jiuwhuichwt')

        response = self.client.get(reverse('core:following', kwargs={'profile_slug': self.user2.profile.slug}))
        friend_request = services.get_friend_request(self.user, self.user2)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(friend_request.to_user, self.user2)
        self.assertEqual(friend_request.from_user, self.user)







