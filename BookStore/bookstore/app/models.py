from django.db import models

# Create your models here.

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
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.firstname

class Promotion(models.Model):
    promocode = models.CharField(max_length=100)
    percentage = models.IntegerField()
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    def __str__(self):
        return self.promocode
