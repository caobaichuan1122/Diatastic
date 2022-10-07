from django.urls import path
from iteration3 import views
urlpatterns = [
    path('', views.index),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('guide/', views.guide, name='guide'),
    path('diary/', views.diary, name='diary'),
    path('ajax/load_portion/', views.load_portion, name='ajax_load_portion'),
    path('ajax/load_cart/', views.load_cart, name='ajax_load_cart'),
    path('ajax/load_description/', views.load_description, name='ajax_load_description'),
    path('create_view/', views.create_view, name='create_view'),
    path('list_view/', views.list_view, name='list_view'),
    path('entry_view/', views.entry_view, name='entry_view'),
    path('please_login/', views.please_login, name='please_login'),
    # path('add_diary/', views.add_diary, name='add_diary'),
    path('carb_chart/', views.carb_chart, name='carb_chart'),
    path('FAQ/', views.FAQ, name='FAQ'),
    path('tips/', views.tips, name='tips'),
]