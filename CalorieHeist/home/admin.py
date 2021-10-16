from django.contrib import admin
from .models import FoodItems, MealNutrients, NutrientsTracking, Notifications

# Register your models here.
admin.site.register(FoodItems)

admin.site.register(MealNutrients)

admin.site.register(NutrientsTracking)

admin.site.register(Notifications)
