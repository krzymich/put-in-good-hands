from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, FormView

from app.forms import RegisterForm
from app.models import Donation, Institution
from django.contrib import messages
from app.models import Donation, Institution, Category


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
        if not request.user.is_authenticated:
            return redirect('login')
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            "categories": categories,
            "institutions": institutions
        }
        return render(request, "form.html", ctx)

    def post(self, request):
        quantity = request.POST.get('bags')
        list_of_categories = request.POST.getlist('categories')
        institution = Institution.objects.get(pk=request.POST.get('organization'))
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('date')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = User.objects.get(username = request.user.username)
        donation = Donation(
            quantity=quantity,
            institution = institution,
            address = address,
            phone_number = phone_number,
            city = city,
            zip_code = zip_code,
            pick_up_date = pick_up_date,
            pick_up_time = pick_up_time,
            pick_up_comment = pick_up_comment,
            user = user
        )
        donation.save()
        for category in list_of_categories:
            donation.categories.add(Category.objects.get(pk=category))
        donation.save()
        return render(request, "form-confirmation.html")

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/login/'

    def form_valid(self, form):
        form.instance.username = form.cleaned_data['email']
        form.instance.password = make_password(form.cleaned_data['password'])
        form.save()
        return super().form_valid(form)

class MyLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        return redirect('register')
