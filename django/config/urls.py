from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from posts.views import PostCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls', namespace='posts')),
    path('comments/', include('comments.urls', namespace='comments')),
    path('users/', include('users.urls', namespace='users')),
    path('users/', include('django.contrib.auth.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
