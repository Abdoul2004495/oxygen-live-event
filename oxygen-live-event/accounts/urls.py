# path() links an address to a view
from django.urls import path
# Django's ready-made login and logout views (we don't need to write them)
from django.contrib.auth import views as auth_views
# Our own views.py (the dot means "same folder")
from . import views

urlpatterns = [
    # Address: /accounts/register/ -> our register view; name lets us refer to it later
    path("register/", views.register, name="register"),
    # Address: /accounts/login/ -> Django's LoginView, using our own template
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    # Address: /accounts/logout/ -> Django's LogoutView
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]