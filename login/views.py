from django.shortcuts import render,redirect
from . import models
import datetime

from .models import diaryentries,calorie


def index(request):
    pass
    return render(request, 'login/index.html')

def prevention(request):
    pass
    return render(request, 'login/prevention.html')

def symptoms(request):
    pass
    return render(request, 'login/symptoms.html')

def community(request):
    pass
    return render(request, 'login/community.html')

def about(request):
    pass
    return render(request, 'login/about.html')

def contact(request):
    pass
    return render(request, 'login/contact.html')

def diary(request):
    pass
    return render(request, 'login/diary.html')

def test(request):
    pass
    return render(request, 'login/test.html')

def add_diary(request):
    pass
    return render(request, 'login/diary.html')