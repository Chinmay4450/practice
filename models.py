from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from phone_field import PhoneField
from django.utils.translation import gettext_lazy as _


# from Employee.models import Employee

class UserInfo(AbstractUser):
    username = models.CharField(_('username'), unique=True, max_length=30)
    email = models.EmailField(_('email address'), unique=True)
    salutation = models.CharField(max_length=10)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, null=True)
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'


choice = (('USD', 'USD'), ('rs', 'rs'))


class Customers(models.Model):
    admin = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    currency = models.CharField(choices=choice, default='USD', max_length=50)
    hospital_name = models.CharField(max_length=50)
    customer_display_name = models.CharField(max_length=50, null=True, blank=True)
    skype_id = models.CharField(max_length=50, null=True, blank=True)
    designation = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=50, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    billing_country = models.CharField(max_length=150, null=True, blank=True)
    billing_state = models.CharField(max_length=150, null=True, blank=True)
    billing_city = models.CharField(max_length=150, null=True, blank=True)
    billing_address_line_one = models.CharField(max_length=150, null=True, blank=True)
    billing_address_line_two = models.CharField(max_length=150, null=True, blank=True)
    billing_address_line_three = models.CharField(max_length=150, null=True, blank=True)
    billing_address_zip = models.CharField(max_length=150, null=True, blank=True)
    shipping_country = models.CharField(max_length=150, null=True, blank=True)
    shipping_state = models.CharField(max_length=150, null=True, blank=True)
    shipping_city = models.CharField(max_length=150, null=True, blank=True)
    shipping_address_line_one = models.CharField(max_length=150, null=True, blank=True)
    shipping_address_line_two = models.CharField(max_length=150, null=True, blank=True)
    shipping_address_line_three = models.CharField(max_length=150, null=True, blank=True)
    shipping_address_zip = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING, null=True, related_name="employee_creator")
    updated_by = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name="employee_modifier")


class Country(models.Model):
    name = models.CharField(max_length=100)


class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class Otpdata(models.Model):
    email = models.EmailField(_('email address'))
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class addnote(models.Model):
    comment = models.CharField(max_length=200)
    created_by = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
