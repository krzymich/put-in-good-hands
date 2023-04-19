from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, FormView

from app.forms import RegisterForm
from app.models import Donation, Institution


# Create your views here.


class IndexView(View):
    def get(self, request):
        no_of_donated_bags = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        no_of_supported_organizations = Donation.objects.values('institution').distinct().count()
        list_of_foundations = Institution.objects.filter(type='FDN')
        list_of_ngos = Institution.objects.filter(type='NGO')
        list_of_local_collections = Institution.objects.filter(type='LC')
        if request.GET.get('ngos_page'):
            active_slide = 2
        elif request.GET.get('lc_page'):
            active_slide = 3
        else:
            active_slide = 1
        foundations_page = request.GET.get('foundations_page')
        foundations_paginator = Paginator(list_of_foundations, 5)
        list_of_5_foundations = foundations_paginator.get_page(foundations_page)
        ngos_page = request.GET.get('ngos_page')
        ngos_paginator = Paginator(list_of_ngos, 5)
        list_of_5_ngos = ngos_paginator.get_page(ngos_page)
        local_collections_page = request.GET.get('local_collections_page')
        local_collections_paginator = Paginator(list_of_local_collections, 5)
        list_of_5_local_collections = local_collections_paginator.get_page(local_collections_page)

        ctx = {
            "no_of_donated_bags": no_of_donated_bags,
            "no_of_supported_organizations": no_of_supported_organizations,
            "list_of_foundations": list_of_5_foundations,
            "list_of_ngos": list_of_5_ngos,
            "list_of_local_collections": list_of_5_local_collections,
            "active_slide" : active_slide
        }
        return render(request, "index.html", ctx)


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/login/'

    def form_valid(self, form):
        form.instance.username = form.cleaned_data['email']
        form.instance.password = make_password(form.cleaned_data['password'])
        form.save()
        return super().form_valid(form)

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
