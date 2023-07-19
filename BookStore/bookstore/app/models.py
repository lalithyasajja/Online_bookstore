import random
from django.db import models
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import UserManager
from datetime import date

# Create your models here.


def random_number_generator():
    return random.randint(100000, 999999)

CATEGORY_CHOICES=(
    ('BIO', 'Biography'),
    ('FIC', 'Fiction'),
    ('HIS', 'History'),
    ('HOR', 'Horror'),
    ('MYS', 'Mystery'),
    ('NOF', 'NonFiction'),
    ('ROM', 'Romance'),
    ('SCI', 'SciFi'),
    ('THR', 'Thriller'),
)

class Book(models.Model):
    ISBN = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='book')
    edition = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    quantity = models.IntegerField()
    minimum_threshold = models.IntegerField()
    buying_price = models.FloatField()
    selling_price = models.FloatField()
    rating = models.IntegerField()
    featured = models.BooleanField(default=False)
    topSeller = models.BooleanField(default=False)
    description = models.TextField(default='null')
    def __str__(self):
        return self.title
    
class User(models.Model):
    account_id = models.IntegerField(unique=True, default=random_number_generator)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    card_number = models.CharField(max_length=80, default=' ')
    expiration_date = models.CharField(max_length=5, default=' ', blank=True)
    security_code = models.CharField(max_length=80, default=' ', blank=True)
    street_address = models.CharField(max_length=50, default=' ', blank=True)
    apartment_suite = models.CharField(max_length=50, default=' ', blank=True)
    city = models.CharField(max_length=30, default=' ', blank=True)
    state = models.CharField(max_length=30, default=' ', blank=True)
    zip_code = models.CharField(max_length=30, default=' ', blank=True)
    contact_phone = models.CharField(max_length=30, default=' ', blank=True)
    contact_email = models.CharField(max_length=30, default=' ', blank=True)
    accept_terms = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_loggedin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=255, blank=True, null=True)
    reset_token = models.CharField(max_length=255, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         # New user, hash the password
    #         self.password = make_password(self.password)
    #     super().save(*args, **kwargs)

    def check_password(self, password):
        return check_password(password, self.password)

    def __str__(self):
        return self.firstname

class Promotion(models.Model):
    promocode = models.CharField(max_length=100)
    percentage = models.IntegerField()
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    def __str__(self):
        return self.promocode
