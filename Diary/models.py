# Diary/models.py

from django.db import models

class User(models.Model):

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    # email = models.EmailField(unique=True)
    # sex = models.CharField(max_length=32,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = 'user'
        verbose_name_plural = 'user'





class Food(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    carbohydrates = models.DecimalField(
        decimal_places=2,
        max_digits=10
    )


class Drink(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    carbohydrates = models.DecimalField(
        decimal_places=2,
        max_digits=10
    )


class DiaryEntries(models.Model):
    diary_id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()

    blood_sugar_level = models.DecimalField(
        decimal_places=2,
        max_digits=5
    )

    food = models.CharField(max_length=120)
    drinks = models.CharField(max_length=120)
