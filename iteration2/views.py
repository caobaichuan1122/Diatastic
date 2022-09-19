from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal
from .models import User, Diary_Menu, Portion, Menu
from .forms import DiaryForm, UserForm, DateForm
from .models import  DiaryEntries
import plotly.express as px


def login(request):
    # if request.session.get('is_login',None):
    #     return redirect('/index/') #sing in page
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "please check！"
        # if login_form.is_valid():
            # username = login_form.cleaned_data['username']
            # password = login_form.cleaned_data['password']
        username = request.POST.get('user')
        password = request.POST.get('password')
        print(User.objects.all())
        try:
            user = User.objects.get(name=username)
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/iteration2/index/')
            else:
                message = "password error！"
        except:
            message = "user error！"
    return render(request, 'iteration2/login.html',{'iteration2':'iteration2'})

def index(request):
    pass
    return render(request, 'iteration2/index.html',{'iteration2':'iteration2'})

def guide(request):
    pass
    return render(request, 'iteration2/Beginners Guide.mht')

def symptoms(request):
    pass
    return render(request, 'iteration2/symptoms.html')

def community(request):
    pass
    return render(request, 'iteration2/community.html')

def about(request):
    pass
    return render(request, 'iteration2/about.html')

def contact(request):
    pass
    return render(request, 'iteration2/contact.html')

def diary(request):
    if request.method == 'GET':
        category = Menu.objects.values('category').distinct()
        portion = Menu.objects.filter(category=category).order_by('portion')
    return render(request, 'iteration2/diary.html',context={'category':category,'portion':portion})

# def porti0n(request):
#     if request.method == "POST":
#         category = request.POST.get('category')
#         if category:
#             portion = Menu.objects.filter(category=category).values('portion')
#     return JsonResponse(portion,safe=False)

def add_diary(request):
    pass
    return render(request, 'iteration2/diary.html')

def test(request):
    pass
    return render(request, 'iteration2/diary.html')

def create_view(request):
    my_form = DiaryForm(request.POST or None)
    if my_form.is_valid():

    # Get form data.
        date = my_form.cleaned_data['date']
        time = my_form.cleaned_data['time']
        blood_sugar_level = my_form.cleaned_data['blood_sugar_level']
        category = my_form.cleaned_data['category']
        portion = my_form.cleaned_data['portion']
        quantity = my_form.cleaned_data['quantity']

    # This will be a list at some point. (carb.append?)
        ## Retrieve carb values for given entry. (.getlist?)
        carbs = Menu.objects.get(category=category,
                                 portion=portion,
                                 ).carbohydrates

        ## Retrieve weight values for given entry.
        weight = Menu.objects.get(category=category,
                                  portion=portion
                                  ).portion_weight

    # Carbohydrate formula.
        carbs = carbs/weight*quantity
        insulin = insulin_calculation(carbs, blood_sugar_level)

    # Updating.
        ## First, update the DiaryEntries model to generate a diary_id.
        DiaryEntries.objects.create(date=date, time=time,
                                    blood_sugar_level=blood_sugar_level,
                                    carbohydrates=0.0,
                                    insulin=0.0)

        # Retrieve generated diary_id.
        id = DiaryEntries.objects.order_by('id').values_list('id', flat=True).last()

        ## Use generated diary_id to populate diary_menu.
        Diary_Menu.objects.create(category=category,
                                  portion=portion,
                                  quantity=quantity,
                                  carbohydrates=carbs
                                  )

        my_form = DiaryForm() # Show stored value.
        context = {
            'form': my_form
        }

        return render(request, 'iteration2/test.html', context)
    else:
        my_form = DiaryForm(request.POST or None)
        context = {
            'form': my_form
        }
    return render(request, 'iteration2/test.html', context)

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

    return render(request, "iteration2/entry_view.html", context)

def list_view(request):
    diary_entry = DiaryEntries.objects.all()
    # for item in diary_entry:
    #     if item.insulin == 0:
    #         DiaryEntries.objects.filter(diary_id =item.diary_id).update(insulin = insulin_calculation(item.food, item.drinks, item.blood_sugar_level))
    return render(request,'iteration2/list_view.html',context={'diary_entry':diary_entry})


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

def get_queryset():
    return DiaryEntries.objects.all().order_by('date')

def please_login(request):
    return render(request, "iteration2/please_login.html")

def page_no_found(request,**kwargs):
    return render(request, "iteration2/404.html")

def load_portion(request):
    category_id = request.GET.get('category')
    portion = Portion.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'iteration2/portion_dropdown_list_options.html', {'portion': portion})

def get_queryset():
    return DiaryEntries.objects.all().order_by('date')
#
# def please_login(request):
#     return render(request, "Diary/404.html")

def carb_chart(request):

    entries = DiaryEntries.objects.all().order_by('-date')
    start = request.GET.get('start')
    end = request.GET.get('end')

    if start:
        entries = entries.filter(date__gte=start)
    if end:
        entries = entries.filter(date__lte=end)

    fig = px.line(
        x=[c.date for c in entries],
        y=[c.carbohydrates for c in entries],
        title = 'Carbohydrates Chart',
        labels={'x': 'Date', 'y': 'Carbohydrates (g)'}
    )

    fig.update_layout(title = {
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5
    })

    carb_chart = fig.to_html()

    context = {'carb_chart': carb_chart,
               'form': DateForm}
    return render(request, 'iteration2/carb_chart.html', context)



