from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

# Create your views here.


class IndexView(View):
    def get(self, request):
        # no_of_donated_bags = Donation.objects.annotate(Sum('quantity'))
        # no_of_supported_organizations = Donation.objects.values('institution').distinct().count()
        # no_of_supported_organizations = len(Donation.objects.values('institution').distinct())
        # list_of_foundations = Institution.objects.filter(type='FDN')
        # list_of_ngos = Institution.objects.filter(type='NGO')
        # list_of_local_collections = Institution.objects.filter(type='LC')
        # foundations_paginator = Paginator(list_of_foundations, 5)
        # foundations_page = request.GET.get('foundations_page')
        # list_of_5_foundations = foundations_paginator.get_page(foundations_page)
        # ngos_paginator = Paginator(list_of_ngos, 5)
        # ngos_page = request.GET.get('ngos_page')
        # list_of_5_ngos = ngos_paginator.get_page(ngos_page)
        # local_collections_paginator = Paginator(list_of_local_collections, 5)
        # local_collections_page = request.GET.get('local_collections_page')
        # list_of_5_local_colletions = local_collections_paginator.get_page(local_collections_page)


        ctx = {
            # "no_of_donated_bags": no_of_donated_bags,
            # "no_of_supported_organizations": no_of_supported_organizations,
            # "list_of_foundations": list_of_foundations,
            # "list_of_ngos": list_of_ngos,
            # "list_of_local_collections": list_of_local_collections,
        }
        return render(request, "index.html", ctx)


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")

class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

class LoginView(View):
    def get(self, request):
        return render(request, "login.html")