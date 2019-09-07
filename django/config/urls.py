from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.urls import path, include


from posts.views import PostCreateView

admins_group, created = Group.objects.get_or_create(name='admins')
editors_group, created = Group.objects.get_or_create(name='editors')
ordinary_users_group, created = Group.objects.get_or_create(name='ordinary_users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls', namespace='posts')),
    path('comments/', include('comments.urls', namespace='comments')),
    path('users/', include('users.urls', namespace='users')),
    path('users/', include('django.contrib.auth.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
