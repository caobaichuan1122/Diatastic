from django.urls import path
from iteration import views
urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('guide/', views.guide, name='guide'),
    path('symptoms/', views.symptoms, name='symptoms'),
    path('community/', views.community, name='community'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('diary/', views.diary, name='diary'),
    path('iteration2/', views.test, name='iteration2'),
    path('create_view/', views.create_view, name='create_view'),
    path('list_view/', views.list_view, name='list_view'),
    path('entry_view/', views.entry_view, name='entry_view'),
    path('please_login/', views.please_login, name='please_login'),
    # path('page_no_found/', views.page_no_found, name='page_no_found'),
]

hander404 = views.page_no_found