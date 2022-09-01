
from django.shortcuts import render, get_object_or_404, redirect

from decimal import Decimal

from .models import Food, Drink, DiaryEntries


import pandas as pd
import ast

from .forms import DiaryForm
from .models import  DiaryEntries


def index(request):
    pass
    return render(request, 'Diary/index.html')

def prevention(request):
    pass
    return render(request, 'Diary/prevention.html')

def symptoms(request):
    pass
    return render(request, 'Diary/symptoms.html')

def community(request):
    pass
    return render(request, 'Diary/community.html')

def about(request):
    pass
    return render(request, 'Diary/about.html')

def contact(request):
    pass
    return render(request, 'Diary/contact.html')

def diary(request):
    pass
    return render(request, 'Diary/diary.html')

def test(request):
    pass
    return render(request, 'Diary/test.html')

def add_diary(request):
    pass
    return render(request, 'Diary/diary.html')

def create_view(request):
    my_form = DiaryForm(request.POST or None)
    if my_form.is_valid():

        date_entered = my_form.cleaned_data['date']
        time_entered = my_form.cleaned_data['time']
        blood_sugar_level = my_form.cleaned_data['blood_sugar_level']
        food = my_form.cleaned_data['food_items']
        drinks = my_form.cleaned_data['drinks']

        p = DiaryEntries(date=date_entered, time=time_entered,
                         blood_sugar_level=blood_sugar_level,
                         food=food, drinks=drinks)
        p.save()
        return redirect("list")
    else:
        my_form = DiaryForm(request.POST or None)
        context = {
            'form': my_form
        }

    return render(request, "Diary/diary.html", context)

def list_view(request):
    queryset = get_queryset()
    context = {
        'object_list': queryset
    }
    return render(request, "Diary/diary.html", context)

def entry_view(request, diary_id):
    obj = get_object_or_404(DiaryEntries, diary_id=diary_id)
    val = insulin_calculation(obj.food, obj.drinks, obj.blood_sugar_level)
    context = {
        'date': obj.date,
        'time': obj.time,
        'food': obj.food,
        'drink': obj.drinks,
        'blood_sugar_level': obj.blood_sugar_level,
        'Insulin': val
    }

    return render(request, "Diary/diary_list.html", context)


def insulin_calculation(food, drinks, blood_sugar_level):
    ## Carbohydrate correction dose.
    # Initialising values.
    carbs = Decimal(0.0)
    target = Decimal(5.0)

    # Retrieving the drink data.
    drinks_data = Drink.objects.all().values()
    drinks_df = pd.DataFrame.from_records(drinks_data)
    drinks_df = drinks_df[drinks_df['name'].isin(ast.literal_eval(drinks))]
    # Retrieving the food data.
    food_data = Food.objects.all().values()
    food_df = pd.DataFrame.from_records(food_data)
    food_df = food_df[food_df['name'].isin(ast.literal_eval(food))]

    # Calculating the carbohydrates.
    carbs += Decimal(sum(food_df['carbohydrates'].values)) + Decimal(sum(drinks_df['carbohydrates'].values))

    # Calculating the carbohydrate balancing dose.
    CHO = carbs/10

    ## High Blood Sugar Correction Dose
    # Initialising the target blood sugar.
    difference = blood_sugar_level - target
    HBSCD = difference/50

    # Final Insulin Dose.
    insulin_req = CHO + HBSCD
    return insulin_req

def get_queryset():
    return DiaryEntries.objects.all().order_by('date')