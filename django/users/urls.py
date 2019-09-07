from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf.urls import url

from .views import SignUpView, activate

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    url(
        r'^activate/(?P<pk>[0-9]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate,
        name='activate'
    ),
]
