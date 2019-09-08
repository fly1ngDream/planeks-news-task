from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.utils import timezone


from .forms import PostForm
from users.models import CustomUser
from .models import Post


class FormsTest(TestCase):

    def test_post_form_valid(self):
        form = PostForm(data={
            'title': 'title1',
            'content': 'content1',
            'created': timezone.now(),
        })
        self.assertTrue(form.is_valid())

    def test_post_form_invalid(self):
        form = PostForm(data={
            'title': 'title1',
            'content': '',
            'created': timezone.now(),
        })
        self.assertFalse(form.is_valid())


class ViewsTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email='user@mail.com',
            username='user',
            password='123321'
        )

    def test_post_list_view(self):
        post = Post.objects.create(
            title='Title1',
            slug='title1',
            author=self.user,
            content='Content1',
            created=timezone.now()
        )
        url = reverse('posts:post_list')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(post.title.encode(), resp.content)
