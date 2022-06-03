import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from airline.models import (Flights)

# Create your models here.
class User(AbstractUser):
    location           = models.CharField(max_length=50, null=True, blank=True)
    phone              = models.CharField(max_length=11, null=True, blank=True)
    flight             = models.ManyToManyField('airline.Flights', related_name='flight', null=True, blank=True)
    card               = models.OneToOneField(
                                'Cards', on_delete=models.DO_NOTHING, related_name='card', null=True, blank=True, db_constraint=False)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "Users"

    def __str__(self):
        return f'{self.username}'


# Create your models here.
class Cards(models.Model):
    cardowner             = models.CharField(max_length=25, null=False, blank=False, default='admin')
    cardnumber            = models.IntegerField(unique=True, null=False, blank=False)
    cvv                   = models.IntegerField(null=False, blank=False)
    expired_date          = models.DateField()
    budget                = models.DecimalField(default=320.50, max_digits=10, decimal_places=2)


    class Meta:
        verbose_name = "cards"
        verbose_name_plural = "Cards"

    def __str__(self):
        return f'{self.cardnumber}'
