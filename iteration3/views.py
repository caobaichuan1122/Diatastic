import json
import os
from datetime import datetime
from django.core import mail
from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal

from numpy import double

from .models import Diary_Menu, Category, Portion, Menu, Description,DiaryEntries
from .forms import  DateForm, EmailForm
from django.contrib.auth.models import User
import plotly
import plotly.express as px
from math import floor
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



def login(request):
    if request.session:
        try:
            id=request.session['_auth_user_id']
            request.session['is_login'] = True
            request.session['signup'] = True
            request.session['user_name'] = User.objects.get(id=id).first_name
            return redirect('/index/')
        except:
            request.session['signup'] = True
            return render(request, 'iteration3/login.html', {'iteration3':'iteration3'})
    else:
        return render(request, 'iteration3/login.html', {'iteration3': 'iteration3'})
    return render(request, 'iteration3/login.html',{'iteration3':'iteration3'})

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return redirect("/index/")


def load_portion(request):
    category_id = request.GET.get('category')
    description_id = request.GET.get('description')
    portion = Portion.objects.filter(category_id=category_id,
                                     description_id=description_id).order_by('name')
    return render(request, 'iteration3/portion_dropdown_list_options.html', {'portion': portion})

def load_description(request):
    category_id = request.GET.get('category')
    description = Description.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'iteration3/description_dropdown_list_options.html', {'description': description})

def diary(request):
    category = Category.objects.values('id', 'name')
    portion = Portion.objects.values('id', 'name')
    description = Description.objects.values('id', 'name')
    return render(request, 'iteration3/diary1.html',
                  context={'category': category,
                           'portion': portion,'description':description})


# Diary views.
def create_view(request):
    if request.method == "POST":
        id = request.session['_auth_user_id']
        cart = request.POST.get('cart_items')
        if len(json.loads(cart)) != 0:
            cart = json.loads(cart)

            # Generate the diary_id.
            DiaryEntries.objects.create(date=cart[0]['date'], time=cart[0]['time'],
                                        blood_sugar_level=cart[0]['BSL'],
                                        carbohydrates=0.0, insulin=0.0,user_id=id)
            # Retrieve the id.
            diaryentries_id = DiaryEntries.objects.filter(date=cart[0]['date'], time=cart[0]['time'],user_id=id).values('id')[0]['id']

            for item in cart:
                category = Category.objects.filter(id=item['categoryId']).values('name')[0]['name']
                description = Description.objects.filter(id=item['descriptionId']).values('name')[0]['name']
                portion = Portion.objects.filter(id=item['portionId']).values('name')[0]['name']
                # Retrieving item carb value, and weight.

                item_carbs = Menu.objects.filter(category=category,
                                                 description=description,
                                                 portion=portion).values('carbohydrates')[0]['carbohydrates']
                item_weight = Menu.objects.filter(category=category,
                                                  description=description,
                                                  portion=portion).values('portion_weight')[0]['portion_weight']
                # Calculate carb value for item.
                item_carbs = item_carbs * item_weight * Decimal(0.01) * item['Q']

                # Update database.
                Diary_Menu.objects.create(diary_id=diaryentries_id,
                                          date=item['date'], time=item['time'],
                                          category=category, description=description, portion=portion, quantity=item['Q'],
                                          carbohydrates=item_carbs,user_id=id)

            # Groupby to get the sum of carbohydrates.
            carbs = Diary_Menu.objects.filter(date=cart[0]['date'], time=cart[0]['time'],
                                              diary_id=diaryentries_id).aggregate(total_sum=Sum('carbohydrates'))
            # Retrieve sum.
            carbs = carbs['total_sum']

            # Get insulin value.
            insulin = insulin_calculation(carbs, cart[0]['BSL'])

            # Update insulin value.
            DiaryEntries.objects.filter(id=diaryentries_id).update(carbohydrates=carbs)
            DiaryEntries.objects.filter(id=diaryentries_id).update(insulin=insulin)
            DiaryEntries.objects.filter(id=diaryentries_id).update(comment=cart[0]['comment'])
            return render(request, 'Diary/list_view.html', context={'cart': cart})
    return render(request, 'iteration3/list_view.html', context={'cart': request.GET.get('cart')})


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

    return render(request, "iteration3/entry_view.html", context)

def list_view(request):
    user_id = request.session['_auth_user_id']
    Entries = DiaryEntries.objects.filter(user_id=user_id).values().all()
    Details = Diary_Menu.objects.values().values_list()
    ListViewDict = {}

    if Entries.exists():
        for item in Entries:
            id = int(item['id'])
            ListViewDict[id] = {'header': [], 'rows': [], 'rows': []}
            ListViewDict[id]['header'] = ['Category', 'Description', 'Portion', 'Quantity', 'Carbohydrates']
            temp = Diary_Menu.objects.filter(diary_id=id).values_list()
            for i in range(len(temp)):
                ListViewDict[id]['rows'].append([temp[i][5], temp[i][6], temp[i][7], temp[i][8], temp[i][9]])
            ListViewDict[id]['insulin'] = floor(DiaryEntries.objects.filter(id=id).values_list('insulin', flat=True)[0])
            ListViewDict[id]['BSL'] = DiaryEntries.objects.filter(id=id).values_list('blood_sugar_level', flat=True)[0]
            comment = DiaryEntries.objects.filter(id=id).values_list('comment', flat=True)[0]
            if not comment:
                DiaryEntries.objects.filter(id=id).update(comment="Date: {}, Time: {}".format(item['date'], item['time']))
            ListViewDict[id]['comment'] = DiaryEntries.objects.filter(id=id).values_list('comment', flat=True)[0]
    context = {
        'field': ListViewDict,
        'details': Details,
    }
    return render(request, 'iteration3/list_view.html', context)

def insulin_calculation(carbs, blood_sugar_level):
    ## Carbohydrate correction dose.
    # Initialising values.
    carbs = Decimal(carbs)
    target = Decimal(5.0)

    # Calculating the carbohydrate balancing dose.
    CHO = carbs/10

    # High Blood Sugar Correction Dose
    ## Initialising the target blood sugar.
    difference = blood_sugar_level - target
    HBSCD = difference/50

    # Final Insulin Dose.
    insulin_req = CHO + HBSCD
    return insulin_req

def carb_chart(request):
    entries = DiaryEntries.objects.filter(user_id=request.session['_auth_user_id']).all().order_by('-date', '-time')
    # If there are entries, check for the start date and end date.
    if entries.exists():
        start = request.GET.get('start')
        end = request.GET.get('end')

        # If start and end date are provided, filter the entries.
        if start and end:
            entries = entries.filter(date__gte=start)
            entries = entries.filter(date__lte=end)
            # If there are entries at that point, create the graph.
            if entries:
                fig1 = px.line(
                    x=[datetime.combine(c.date, c.time) for c in entries],
                    y=[c.blood_sugar_level for c in entries],
                    title='Blood Sugar Chart',
                    labels={'x': 'Date', 'y': 'Blood Sugar (mmol/L)'}
                )
                fig2 = px.line(
                    x=[datetime.combine(c.date, c.time) for c in entries],
                    y=[c.carbohydrates for c in entries],
                    title='Carbohydrates Chart',
                    labels={'x': 'Date', 'y': 'Carbohydrates (g)'}
                )
                fig3 = px.line(
                    x=[datetime.combine(c.date, c.time) for c in entries],
                    y=[c.insulin for c in entries],
                    title='Insulin Chart',
                    labels={'x': 'Date', 'y': 'Insulin (units)'}
                )
            # If no entries, return 0.
            else:
                fig1 = px.line(
                    x=[0],
                    y=[0],
                    title='Blood Sugar Chart',
                    labels={'x': 'Date', 'y': 'Blood Sugar (mmol/L)'}
                )
                fig2 = px.line(
                    x=[0],
                    y=[0],
                    title='Carbohydrates Chart',
                    labels={'x': 'Date', 'y': 'Carbohydrates (g)'}
                )
                fig3 = px.line(
                    x=[0],
                    y=[0],
                    title='Insulin Chart',
                    labels={'x': 'Date', 'y': 'Insulin (units)'}
                )
        # If no dates are provided, return all entries.
        else:
            fig1 = px.line(
                x=[datetime.combine(c.date, c.time) for c in entries],
                y=[c.blood_sugar_level for c in entries],
                title='Blood Sugar Chart',
                labels={'x': 'Date', 'y': 'Blood Sugar (mmol/L)'}
            )
            fig2 = px.line(
                x=[datetime.combine(c.date, c.time) for c in entries],
                y=[c.carbohydrates for c in entries],
                title='Carbohydrates Chart',
                labels={'x': 'Date', 'y': 'Carbohydrates (g)'}
            )
            fig3 = px.line(
                x=[datetime.combine(c.date, c.time) for c in entries],
                y=[c.insulin for c in entries],
                title='Insulin Chart',
                labels={'x': 'Date', 'y': 'Insulin (units)'}
            )
    # If no entries, return 0.
    else:
        fig1 = px.line(
            x=[0],
            y=[0],
            title='Blood Sugar Chart',
            labels={'x': 'Date', 'y': 'Blood Sugar (mmol/L)'}
        )
        fig2 = px.line(
            x=[0],
            y=[0],
            title='Carbohydrates Chart',
            labels={'x': 'Date', 'y': 'Carbohydrates (g)'}
        )
        fig3 = px.line(
            x=[0],
            y=[0],
            title='Insulin Chart',
            labels={'x': 'Date', 'y': 'Insulin (units)'}
        )

    fig1.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)")

    fig2.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)")

    fig3.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)")

    bsl_chart = fig1.to_html()
    carb_chart = fig2.to_html()
    insulin_chart = fig3.to_html()

    try:
        os.makedirs('../tp08_website/attachments/{}'.format(request.session['_auth_user_id']))
        fig1.write_html("../tp08_website/attachments/{}/fig_bsl.html".format(request.session['_auth_user_id']))
        fig2.write_html("../tp08_website/attachments/{}/fig_carb.html".format(request.session['_auth_user_id']))
        fig3.write_html("../tp08_website/attachments/{}/fig_isl.html".format(request.session['_auth_user_id']))
    except:
        fig1.write_html("../tp08_website/attachments/{}/fig_bsl.html".format(request.session['_auth_user_id']))
        fig2.write_html("../tp08_website/attachments/{}/fig_carb.html".format(request.session['_auth_user_id']))
        fig3.write_html("../tp08_website/attachments/{}/fig_isl.html".format(request.session['_auth_user_id']))
    context = {'bsl_chart': bsl_chart,
               'carb_chart': carb_chart,
               'insulin_chart': insulin_chart,
               'form': DateForm}
    return render(request, 'iteration3/carb_chart.html', context)

def email_form(request):
    form = EmailForm(request.POST or None)
    user_name = request.session['user_name']
    return render(request, 'iteration3/mail.html',context={'form':form,'user_name':user_name})

def success(request):
    subject = request.POST['subject']
    email_message = request.POST['message']
    email = request.POST['email']
    try:
        validate_email(email)
    except ValidationError:
        message = 'Bad email'
        return render(request, 'iteration3/mail.html',
                      {'message':message})
    else:
        message = 'Send successful！'
        connection = mail.get_connection()
        if connection:
            email = mail.EmailMessage(subject, email_message, settings.EMAIL_HOST_USER, [email])
            email.attach_file("../tp08_website/attachments/{}/fig_bsl.html".format(request.session['_auth_user_id']))
            email.attach_file("../tp08_website/attachments/{}/fig_carb.html".format(request.session['_auth_user_id']))
            email.attach_file("../tp08_website/attachments/{}/fig_isl.html".format(request.session['_auth_user_id']))
            email.send()
            return render(request, 'iteration3/mail.html',{'message':message})
        else:
            message = 'Could not connect to the mail server. Please try again later.'
            return render(request, 'iteration3/mail.html',{'message':message})


def load_cart(request):
    cart = request.POST.get('cart_items')
    cart = json.loads(cart)
    return render(request, 'iteration3/diary.html', {'cart':cart})

def get_queryset():
    return DiaryEntries.objects.all().order_by('date')

def please_login(request):
    return render(request, "iteration3/please_login.html")

def page_no_found(request,**kwargs):
    return render(request, "iteration3/404.html")

def index(request):
    if request.session:
        try:
            entries = DiaryEntries.objects.filter(user_id=request.session['_auth_user_id']).all().order_by('-date', '-time')
            y_bsl = str([double(c.blood_sugar_level) for c in entries])
            y_carb = str([double(c.carbohydrates) for c in entries])
            y_isl = str([double(c.insulin) for c in entries])
            return render(request, 'iteration3/index.html', {'y_bsl': y_bsl,'y_carb': y_carb,'y_isl': y_isl})
        except:
            request.session['signup'] = True
            return render  ( request,'iteration3/index.html', {'iteration3':'iteration3'})
    else:

        return render(request, 'iteration3/index.html',{'iteration3':'iteration3'})

def guide(request):
    pass
    return render(request, 'iteration3/Beginners Guide.html')

def FAQ(request):
    pass
    return render(request, 'iteration3/faq.html')

def tips(request):
    pass
    return render(request, 'iteration3/tips.html')

def add_list(request):
    pass
    return render(request, 'iteration3/add.html')





