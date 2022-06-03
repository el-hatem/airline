from django.urls import path
from django.contrib.auth.decorators import login_required
from users.views import (
    LoginView,
    RegisterView,
    logout_view,
    ProfileView,
    delete_card,
    add_card
)

app_name = 'users'

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", logout_view, name="logout"),
    path("register", RegisterView.as_view(), name="register"),
    path('addcard',add_card, name='addcard'),
    path('deletecard',delete_card, name='deletecard'),
    path("me", login_required(ProfileView.as_view(), login_url="users:login"), name="profile")
]
