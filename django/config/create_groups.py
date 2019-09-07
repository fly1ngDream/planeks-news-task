from django.contrib.auth.models import Group


def create_groups():
    admins_group, created = Group.objects.get_or_create(name='admins')
    editors_group, created = Group.objects.get_or_create(name='editors')
    ordinary_users_group, created = Group.objects.get_or_create(name='ordinary_users')
