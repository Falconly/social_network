from django.test import TestCase
from django.urls import reverse

from core.tests import BaseTest

from posts import factories, models


# Create your tests here.
class PostsTest(BaseTest, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.category = factories.Category()
        self.post = factories.Post(user=self.user, profile=self.user.profile, to_user=self.user2,
                                   category=self.category)
        self.comment = factories.Comment(user=self.user, profile=self.user.profile, post=self.post)

    def test_delete_post(self):
        self.client.login(username='Login2', password='er2jiuwhuichwt')

        response = self.client.get(reverse('posts:delete_post', kwargs={'post_pk': self.post.pk}))
        posts = models.Posts.objects.posts(self.user)

        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.post, posts)

    def test_update_post(self):
        self.client.login(username='Login2', password='er2jiuwhuichwt')
        form_data = {
            'content': 'Hello World!',
            'category': self.category.pk,
            'user': self.user.pk,
            'profile': self.user.profile.pk,
            'to_user': self.user2.pk,
        }

        response = self.client.post(reverse('posts:update_post', kwargs={'post_pk': self.post.pk}), data=form_data)

        self.assertEqual(response.status_code, 302)
        post = models.Posts.objects.post(self.post.pk)
        self.assertEqual(post.content, form_data['content'])

    def test_delete_comment(self):
        self.client.login(username='Login2', password='er2jiuwhuichwt')

        response = self.client.get(reverse('posts:delete_comment', kwargs={'comment_pk': self.comment.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.comment, models.Comments.objects.all())
