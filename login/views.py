from django.shortcuts import render,redirect
from . import models
import datetime

from .models import diaryentries,calorie


def index(request):
    pass
    return render(request, 'login/index.html')



def test(request):
    foods = diaryentries.objects.all()
    print(foods)
    return render(request, 'login/test.html')