from django.urls import path
from iteration2 import views
urlpatterns = [
    path('', views.login),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('please_login/', views.please_login, name='please_login'),
]