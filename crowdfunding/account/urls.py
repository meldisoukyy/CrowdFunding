from django.urls import path, include
from django.contrib.auth import views
from .views import (
    socialHomeView,
    register,
    activate,
    signin
)

urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
    path('social',socialHomeView,name='social_home'),
    # path('auth/',include('django.contrib.auth.urls')),
    path('register/',register, name='register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        activate, name='activate'),
    path('login/', signin, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('',include('password.urls')),
]
