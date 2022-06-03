import random as rd
from datetime import datetime as dt
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.template.defaulttags import register
from django.views.generic import View
from airline.models import (Flights)
from booksystem.models import (Payment)
from users.models import (User)

classes = {1: 'Economics', 2: 'Business',
           3: 'Family Trip', 4: 'volunteering', 5: 'Tourism'}
states = {0: 'One way', 1: 'Returned'}

class FlightsView(View):

  def post(self, request, *args, **kwargs):
    filters = { key: value
                for key, value in request.POST.items()
                if key in ['state', 'origin', 'dist', 'dept_date', 'return_date', 'price__lte', 'trip_class'] and value != ''}
    flights = Flights.objects.filter(**filters).all()
    return render(request, 'booksystem/search.html', {'flights': flights, 'classes': classes, 'states': states})


class SearchView(View):
  template_name = "booksystem/search.html"

  def get(self, request, *args, **kwargs):

    flights = Flights.objects.all()
    return render(request, self.template_name, {'flights': flights, 'classes': classes, 'states': states})


class BookView(View):
  template_name = "booksystem/book.html"

  def get(self, request, *args, **kwargs):
    todays_date = dt.now().date()

    flight = Flights.objects.get(pk=kwargs['id'])
    if todays_date > flight.dept_date:
      messages.warning(request, "this flight is not bookable. Search for available Flights.")
      return redirect(reverse('booksystem:search'))

    return render(request, self.template_name, {'flight': flight, 'classes': classes, 'states': states})

  def post(self, request, *args, **kwargs):
    flight = Flights.objects.get(pk=kwargs['id'])
    user = User.objects.get(username=request.user.username)
    card = user.card
    total_price = flight.price * int(request.POST['amount'])
    if flight not in list(user.flight.all()):
      if total_price < card.budget:
        payment = Payment(code=f'P-{rd.randint(10000, 999999)}', payer=user, flight=flight, 
                          amount=request.POST['amount'], price=total_price)
        card.budget -= total_price
        user.flight.add(flight)
        payment.save()        
        user.save()
        card.save()
        return redirect(reverse('users:profile') + '#bill')
      else:
        messages.error(request, "You don't have enough money.")
        return redirect(reverse('booksystem:book', args=[flight.id]))
    else:
      messages.error(request, "Already have this flight booked.")
      return redirect(reverse('booksystem:book', args=[flight.id]))


class DeletePaymentView(View):

  def post(self, request, *args, **kwargs):
    payment = Payment.objects.get(pk=kwargs['payid'])
    user = User.objects.get(username=payment.payer.username)
    flight = Flights.objects.get(pk=payment.flight.id)

    user.flight.set(user.flight.exclude(id=flight.id).all())
    try:
      user.card.budget += payment.price
      user.card.save()
      user.save()
      payment.delete()
      messages.success(request, "Payment Delete cashback added to your card successfully.")
      return redirect(reverse('users:profile') + '#bill')
    except:
      user.save()
      payment.delete()
      messages.warning(request, "You do not have credit card check your email for cashback details.")
      return redirect(reverse('users:profile') + '#bill')


@login_required(login_url="users:login")
@require_http_methods("POST")
def delay(request, payid, flightid):
  addmessage = ''
  payment = Payment.objects.get(pk=payid)
  user = User.objects.get(username=payment.payer.username)
  newflight = Flights.objects.get(pk=flightid)

  if newflight not in list(user.flight.all()):
    price = payment.flight.price - newflight.price

    try:
        user.card.budget += price
        if user.card.budget >= 0:
          user.card.save()
          user.flight.set(user.flight.exclude(id=payment.flight.id).all())
          user.flight.add(newflight)
          payment.flight = newflight
          user.save()
          payment.save()
          messages.success(request, "Flight delayed successfully")
          return redirect(reverse("users:profile")+"#bill")
        else:
          messages.error(request, "Do not have money to confirm delay. please contact us")
          return redirect(reverse("users:profile")+"#bill")

    except:
      if price >= 0:
        payment.flight = newflight
        user.flight.set(user.flight.exclude(id=payment.flight.id).all())
        user.flight.add(newflight)
        user.save()
        payment.save()
        messages.success(request, "Flight delayed successfully. check email for cashback details")
        return redirect(reverse("users:profile")+"#bill")
      else:
        messages.error(request, "Do not have money to confirm delay. please contact us")
        return redirect(reverse("users:profile")+"#bill")
  else:
    messages.error(request, "Already on the flight")
    return redirect(reverse("users:profile")+"#bill")


@register.filter
def available_flights(payment):
  flights = Flights.objects.filter(origin=payment.flight.origin, dist=payment.flight.dist,
      trip_class=payment.flight.trip_class, state=payment.flight.state, dept_date__gt=dt.now().date()).all()

  print(payment)
  return flights



@register.filter
def get_item(dictionary, key):
  return dictionary.get(key)

@register.simple_tag
def random_int(a=1, b=1000):
    if b is None:
        a, b = 0, a
    return rd.randint(a, b)