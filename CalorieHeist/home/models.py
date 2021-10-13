import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class FoodItems(models.Model):
    username = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100)
    calorie = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    image = models.ImageField(
        upload_to="foodItems/images", null=True, blank=True)
    favorite = models.ManyToManyField(
        User, related_name="favorite", blank=True)

    def __str__(self):
        return self.name


class MealNutrients(models.Model):
    username = models.CharField(max_length=100, default="")
    day = models.DateField(default=timezone.now)
    meal = models.CharField(max_length=100)
    calorie = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    fiber = models.FloatField()


class NutrientsTracking(models.Model):
    username = models.CharField(max_length=100, default="")
    date = models.DateField(default=timezone.now)
    day = models.AutoField(primary_key=True)
    calorie = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    fiber = models.FloatField()


class Notifications(models.Model):
    message = models.TextField()
    time = models.TimeField()
