from django.urls import path, include


from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    attachment_download_view,
    subscribe_view,
    unsubscribe_view,
)


app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path(
        '<slug:slug>/subscribe/<int:pk>',
        subscribe_view,
        name='subscribe',
    ),
    path(
        '<slug:slug>/unsubscribe/<int:pk>',
        unsubscribe_view,
        name='unsubscribe',
    ),
    path(
        '<slug:slug>/attachment/download',
        attachment_download_view,
        name='attachment_download'
    ),
    path('<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
