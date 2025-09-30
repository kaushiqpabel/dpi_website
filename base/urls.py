from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
  path("", views.homePage, name="homePage"),
  path("user/<str:pk>/", views.userPage, name="userPage"),
  path("user-form/", views.userFormPage, name="userFormPage"),
  path("get-reg-key/", views.getRegKeyPage, name="getRegKeyPage"),
  path('login/', views.loginPage, name="login"),
  path('logout/', views.logoutUser, name="logout"),
  path('change-password/', views.changePassword, name="changePassword"),
  path('register/', views.registerPage, name="register"),
  path('send-otp/', views.sendOTP, name='sendOTP'),
  path('verify-otp', views.verifyOTP, name='verifyOTP'),
  path('reset-password/', views.MyPasswordResetView.as_view(extra_context={'page': 'page'}), name='reset_password'),
  path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='base/reset_password/success_message.html', extra_context={'page': 'page', 'linkSend':'linkSend'}), name='password_reset_done'),
  path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(template_name='base/reset_password_form.html', extra_context={'page': 'page'}), name='password_reset_confirm'),
  path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='base/reset_password/success_message.html', extra_context={'page': 'page'} ), name='password_reset_complete'),
]