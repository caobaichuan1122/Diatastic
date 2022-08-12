from time import timezone

from django.shortcuts import render,redirect
from . import models
import datetime as dt
from login.models import Weather


def index(request):
    weather_list = Weather.objects.filter(postcode=3000).values_list()
    time = dt.datetime.now()
    print(weather_list[0][1],time)
    return render(request, 'login/index.html')

def load_weather(request):
    weather_list = models.Weather.objects.all()
    weather_list_2 = models.Weather_2.objects.all()
    print(weather_list[0])

def enter_postcode(request):
    if request.method == "POST":
        post_code = request.POST.get('postcode')
        print(post_code)
    return post_code