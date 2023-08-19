from django.urls import path
from django.contrib.auth import views as auth_views

from .forms import LoginForm
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('accounts/profile/', views.profile, name='accounts-profile'),

    # Change Password
    path('change_password/', views.PasswordChangeView.as_view(template_name = "core/password_change.html"), name="change-password"),
    path('password_success/', views.password_success, name="password_success"),
]