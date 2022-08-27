from django.shortcuts import render,redirect
from . import models
import datetime
from login.models import Weather


def index(request):
    pass
    return render(request, 'login/index.html')

def test(request):
    pass
    return render(request, 'login/test.html')

def load_weather(request):
    weather_list = models.Weather.objects.all()
    weather_list_2 = models.Weather_2.objects.all()
    print(weather_list)

def enter_postcode(request):
    if request.method == "POST":
        post_code = request.POST.get('postcode')
        print(post_code)
    return post_code