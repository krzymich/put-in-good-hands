from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64)


class Institution(models.Model):
    FOUNDATION = "FDN"
    NGO = "NGO"
    LOCAL_COLLECTION = "LC"

    INSTITUTION_TYPE_CHOICES = [
        (FOUNDATION, "fundacja"),
        (NGO, "organizacja pozarządowa"),
        (LOCAL_COLLECTION, "zbiórka lokalna")
    ]
    name = models.CharField()
    description = models.TextField()
    type = models.CharField(choices=INSTITUTION_TYPE_CHOICES, default=FOUNDATION)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=64)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.SET_NULL)
