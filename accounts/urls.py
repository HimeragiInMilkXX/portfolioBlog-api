from django.urls import path
from .views import ProfileUpdateView, RegisterView, LoginView, LogoutView, ProfileAvatarView, csrf, MeView

urlpatterns = [
    path( 'auth/csrf', csrf, name="csrf" ),
    path( 'auth/me', MeView.as_view(), name="me"),
    path( 'auth/update', ProfileUpdateView.as_view(), name="update" ),
    path( 'auth/register', RegisterView.as_view(), name="register" ),
    path( 'auth/login', LoginView.as_view(), name="login" ),
    path( 'auth/logout', LogoutView.as_view(), name="logout" ),
    path( 'image/avatar', ProfileAvatarView.as_view(), name="avatar-upload" ),
]