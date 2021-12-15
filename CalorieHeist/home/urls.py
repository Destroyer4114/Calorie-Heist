from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.loginUser, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logoutUser, name="logout"),
    path("addToFavorites/<int:id>", views.addToFavorites, name="addToFavorites"),
    path("favorites", views.favorites, name="favorites"),
    path("trackingMealNutrients", views.trackingMealNutrients,
         name="trackingMealNutrients"),
    path("trackingNutrients", views.trackingNutrients, name="trackingNutrients"),
    path("addFoodItems", views.addFoodItems, name="addFoodItems"),
    path("weekly", views.weekly, name="weekly"),
    path("monthly", views.monthly, name="monthly"),
    path("calorieNeed", views.calorieNeed, name="calorieNeed"),
    path("calorieCalculator", views.calorieCalculator, name="calorieCalculator"),
    path("healthTip", views.healthTip, name="healthTip"),
    path("portfolio", views.portfolio, name="portfolio"),
    path("workout", views.workout, name="workout"),
    path("activitySelection", views.activitySelection, name="activitySelection"),
]
