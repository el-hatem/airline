from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from booksystem.views import (
    FlightsView,
    SearchView,
    BookView, 
    DeletePaymentView,
    delay
)

app_name = 'booksystem'

urlpatterns = [
    path("flights", FlightsView.as_view(), name="flights"),
    path("search", SearchView.as_view(), name="search"),
    re_path('^delete_payment/(?P<payid>[0-9]+)/$', login_required(DeletePaymentView.as_view(), login_url="users:login"), name='delete_payment'),
    re_path('^book/(?P<id>[0-9]+)/$', login_required(BookView.as_view(), login_url="users:login"), name='book'),
    re_path('^delay/(?P<payid>[0-9]+)/(?P<flightid>[0-9]+)$', delay, name='delay')

]
