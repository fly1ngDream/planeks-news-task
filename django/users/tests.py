from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')

        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIn(user, User.objects.filter(groups__name='ordinary_users'))

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')

        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIn(admin_user, User.objects.filter(groups__name='admins'))

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)


class DefaultGroupsTest(TestCase):

    def test_default_groups(self):
        default_group_names = ['admins', 'editors', 'ordinary_users']
        group_names = Group.objects.values_list('name', flat=True)
        [self.assertIn(n, group_names) for n in default_group_names]
