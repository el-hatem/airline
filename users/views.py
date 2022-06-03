from datetime import datetime
import random as rd
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import View
from users.models import User
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from booksystem.models import (Payment)
from users.models import (Cards)

payment_methods = {0: 'Credit Cards', 1: 'Paybal', 2: 'Bank Account'}
status = {0: 'failed', 1:'success', 2: 'pending'}


class LoginView(View):
    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST["login-user"]
        password = request.POST["login-pass"]
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("airline:index")
        else:
            messages.error(request, "Invalid username and/or password.")
            return redirect("users:login")


class RegisterView(View):
    template_name = "users/register.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["pass1"]
        confirmation = request.POST["pass2"]
        location = request.POST["location"]
        phone = request.POST["phone"]


        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return redirect('users:register')
        # Attempt to create new user
        try:
            user = User(email=email, username=username, password=make_password(password), location=location, phone=phone)
            user.save()
            login(request, user)
            return redirect("airline:index")
        except IntegrityError:
            messages.error(request, "Username already taken.")
            return redirect('users:register')


@login_required(login_url="users:login")
@require_http_methods("POST")
def add_card(request):
    inputs = { key: value
                for key, value in request.POST.items()
                if key in ['owner', 'card-number', 'expired-date', 'cvv']}
    inputs['expired-date'] = inputs['expired-date'] + '-1'

    try:
        card = Cards.objects.get(cardnumber=inputs['card-number'])
        messages.error(request, "This card already exists for another user.")
        return redirect(reverse('users:profile') + '#bill')

    except:
        user = User.objects.get(username=request.user.username)
        try:
            user.card.delete()
            card = Cards(cardowner=inputs['owner'], cardnumber=inputs['card-number'],
                expired_date=inputs['expired-date'], cvv=inputs['cvv'], budget=rd.uniform(300.80, 2400.90))
            card.save()
            user.card = card
            user.save()
        except:
            card = Cards(cardowner=inputs['owner'], cardnumber=inputs['card-number'],
                expired_date=inputs['expired-date'], cvv=inputs['cvv'], budget=rd.uniform(300.80, 2400.90))
            card.save()
            user.card = card
            user.save()
        messages.success(request, "Card added successfully")
        return redirect(reverse("users:profile")+"#bill")


@login_required(login_url="users:login")
@require_http_methods("POST")
def delete_card(request):
    user = User.objects.get(username=request.user.username)
    try:
        user.card.delete()
        messages.success(request, "Card deleted successfully")
        return redirect(reverse("users:profile")+"#bill")
    except:
        messages.error(request, "No added Cards to delete")
        return redirect(reverse("users:profile")+"#bill")


class ProfileView(View):
    template_name = "users/settings.html"

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        payments = Payment.objects.filter(payer=user).all()
        return render(request, self.template_name, {'payments': payments, 'method': payment_methods, 'status': status})

@login_required
def logout_view(request):
    logout(request)
    return redirect("airline:index")
