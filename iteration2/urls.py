from django.urls import path
from iteration2 import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('test/', views.test, name='test'),
]