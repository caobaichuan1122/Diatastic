from django.shortcuts import render, redirect

# Create your views here.
from iteration2.forms import UserForm
from iteration2 import models


def index(request):
    pass
    return render(request, 'iteration2/index.html')

def test(request):
    pass
    return render(request, 'iteration2/test.html')


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
        try:
            user = models.User.objects.get(name=username)
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/iteration2/index/')
            else:
                message = "password error！"
        except:
            message = "user error！"
    return render(request, 'iteration2/login.html', locals())