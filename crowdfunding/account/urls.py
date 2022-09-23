from django.urls import path, include
from django.contrib.auth import views
from .views import (
    socialHomeView,
    register,
    activate,
    signin,
    ViewProfile,
    ViewProfileDonations,
    UpdateAccountView,
    Dashboard,
    feature_it,
)

urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
    path('social',socialHomeView,name='social_home'),
    path('register/',register, name='register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        activate, name='activate'),
    path('login/', signin, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('view_profile/<int:pk>', ViewProfile.as_view(), name='view_profile'),
    path('view_profile/donations/<int:pk>', ViewProfileDonations.as_view(), name='view_profile_donations'),
    path('edit_profile/<int:pk>', UpdateAccountView.as_view(), name='edit_profile'),
    path('dashboard/<int:pk>', Dashboard.as_view(), name='dashboard'),
    path('',include('password.urls')),
    path('feature_id/', feature_it, name='feature_it'),
]
