from django.contrib import admin
from airline.models import (
    Flights, Airline
)
# Register your models here.
admin.site.register(Flights)
admin.site.register(Airline)