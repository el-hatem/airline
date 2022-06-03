import random as rd
from datetime import datetime as dt
from django.db import models

# Create your models here.
class Payment(models.Model):
    code                  = models.CharField(max_length=9, null=False, blank=False, default=f'P-{rd.randint(10000, 99999)}')
    amount                = models.IntegerField(null=False, blank=False)
    method                = models.IntegerField(null=False, blank=False, default=0)
    status                = models.IntegerField(null=False, blank=False, default=1)
    date                  = models.DateField(default=dt.now())
    price                 = models.DecimalField(max_digits=10, decimal_places=2) 
    payer                 = models.ForeignKey('users.User', related_name='user', on_delete=models.CASCADE)
    flight                = models.ForeignKey('airline.Flights', related_name='bill', on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)

    class Meta:
        verbose_name = "payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f'{self.code}'
