from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as av
from .views import signup, otp_verification

urlpatterns = [
    path('accounts/signup/', signup, name='signup'),
    path('accounts/login/', av.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', av.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    # path('accounts/<int:pk>', av.UserProfileView.as_view(), name='user_profile'),
    # path('accounts/profile/<int:pk>', av.UserProfileView.as_view()),
    path('accounts/signup/otp', otp_verification, name='otp_verification' )
    # path('accounts/signup/', BaseRegisterView.as_view(template_name='accounts/signup.html'), name='signup'),
    # path('accounts/signup/', )
]