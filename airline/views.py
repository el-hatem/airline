from django.shortcuts import render
from django.views.generic import View


# Create your views here.
class IndexView(View):
    template_name = "airline/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ContactsView(View):
    template_name = "airline/contacts.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SafetyView(View):
    template_name = "airline/safety.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ChartersView(View):
    template_name = "airline/charters.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ServicesView(View):
    template_name = "airline/services.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)