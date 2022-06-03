import random
from django.db import models
from booksystem.models import (
    Payment
)

# Create your models here.
class Flights(models.Model):
    code                  = models.CharField(max_length=7, null=False, blank=False, default=f'F-{random.randint(10000, 99999)}')
    origin                = models.CharField(max_length=100, null=False, blank=False)
    dist                  = models.CharField(max_length=100, null=False, blank=False)
    trip_class            = models.IntegerField(default=3)
    state                 = models.IntegerField(default=0)
    dept_date             = models.DateField()
    dept_time             = models.TimeField()
    return_date           = models.DateField(null=True, blank=True)
    return_time           = models.TimeField(null=True, blank=True)
    airline               = models.ForeignKey('Airline', related_name='airline', on_delete=models.CASCADE)
    price                 = models.DecimalField(default=round(random.uniform(100.0, 501.0), 2), 
    											max_digits=10, decimal_places=2) 
    class Meta:
        verbose_name = "flights"
        verbose_name_plural = "Flights"

    def __str__(self):
        return f'Flight from: {self.origin} to: {self.dist}'


class Airline(models.Model):
    name                = models.CharField(max_length=100, null=False, blank=False)
    country             = models.CharField(max_length=100, null=False, blank=False)
    image               = models.URLField(max_length=1024, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "airline"
        verbose_name_plural = "Airline"

    def __str__(self):
        return f'Airline: {self.name}'
