from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as av
from .views import signup, otp_verification, UserProfileView

urlpatterns = [
    path("accounts/signup/", signup, name="signup"),
    path(
        "accounts/login/",
        av.LoginView.as_view(template_name="account/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        av.LogoutView.as_view(template_name="account/logout.html"),
        name="logout",
    ),
    path("accounts/<int:pk>", UserProfileView.as_view(), name="user_profile"),
    path("accounts/signup/otp", otp_verification, name="otp_verification"),
]
