# login/models.py

from django.db import models

class User(models.Model):

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    # email = models.EmailField(unique=True)
    # sex = models.CharField(max_length=32,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = 'user'
        verbose_name_plural = 'user'

class diaryentries(models.Model):
    date = models.DateField(max_length=6)
    time = models.TimeField(max_length=6)
    blood_sugar_level = models.DecimalField(max_digits=65,decimal_places = 5)
    food = models.CharField(max_length=256)
    drinks = models.CharField(max_length=256)

class calorie(models.Model):
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=256)
    carbohydrates = models.DecimalField(max_digits=65,decimal_places = 5)
