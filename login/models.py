# login/models.py

from django.db import models


class User(models.Model):

    #create the user info
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = 'user'
        verbose_name_plural = 'user'

class Weather(models.Model):

    #create the user info
    postcode = models.IntegerField(unique=True,primary_key=True)
    timestamp = models.DateTimeField()
    temp = models.FloatField()
    uv = models.FloatField()

class Weather_2(models.Model):

    #create the user info
    postcode = models.IntegerField(unique=True,primary_key=True)
    timestamp = models.DateTimeField()
    temp = models.FloatField()
    uv = models.FloatField()