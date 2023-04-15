from django.shortcuts import render
from django.views import View

# Create your views here.


class IndexView(View):
    def get(self, request):
        return render(request, "index.html")

class IndexViewOld(View):
    def get(self, request):
        return render(request, "index-old.html")

class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")

class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")