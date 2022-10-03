# iteration3/models.py

from django.db import models
from django.core.validators import MinValueValidator

# User
class User(models.Model):
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'user'
        app_label = "iteration3"

class Category(models.Model):
    name = models.CharField(max_length=1280)
    def __str__(self):
        return self.name

class Portion(models.Model):
    name = models.CharField(max_length=1280)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Description(models.Model):
    name = models.CharField(max_length=1280)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Menu
class Menu(models.Model):
    category = models.CharField(max_length=1280)
    portion = models.CharField(max_length=1280)
    description = models.CharField(max_length=1280)
    portion_weight = models.DecimalField(max_digits=10,
                                         decimal_places=2)

    carbohydrates = models.DecimalField(
        decimal_places=2,
        max_digits=6
    )


class DiaryEntries(models.Model):
    date = models.DateField()
    time = models.TimeField()

    blood_sugar_level = models.DecimalField(
        decimal_places=2,
        max_digits=5
    )

    carbohydrates = models.DecimalField(
        decimal_places=2,
        max_digits=10
    )

    insulin = models.DecimalField(
        decimal_places=2,
        max_digits=5
    )

# Diary_Menu - Stores each item separately, and records the individual carb value.
class Diary_Menu(models.Model):
    id = models.AutoField(primary_key=True)
    diary = models.ForeignKey(DiaryEntries, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    category = models.CharField(max_length=1280)
    description = models.CharField(max_length=1280)
    portion = models.CharField(max_length=1280)

    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    carbohydrates = models.DecimalField(decimal_places=2,
                                        max_digits=10)
    class Meta:
        ordering = ['date', 'time']