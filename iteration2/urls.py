from django.urls import path
from iteration2 import views
urlpatterns = [
    path('', views.login, name='iteration2/login'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('guide/', views.guide, name='guide'),
    path('symptoms/', views.symptoms, name='symptoms'),
    path('community/', views.community, name='community'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('diary/', views.diary, name='diary'),
    path('ajax/load_portion/', views.load_portion, name='ajax_load_portion'),
    path('test/', views.test, name='test'),
    path('create_view/', views.create_view, name='create_view'),
    path('list_view/', views.list_view, name='list_view'),
    path('entry_view/', views.entry_view, name='entry_view'),
    path('please_login/', views.please_login, name='please_login'),
    path('add_diary/', views.add_diary, name='add_diary'),
    path('carb_chart/', views.carb_chart, name='carb_chart'),
]