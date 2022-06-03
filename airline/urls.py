from django.urls import path
from django.contrib.auth.decorators import login_required
from airline.views import (
    IndexView,
    ContactsView,
    SafetyView,
    ChartersView,
    ServicesView,
)

app_name = 'airline'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contacts", ContactsView.as_view(), name="contacts"),
    path("safety", SafetyView.as_view(), name="safety"),
    path("charters", ChartersView.as_view(), name="charters"),
    path("services", ServicesView.as_view(), name="services")
]
