# from win10toast import ToastNotifier
from datetime import date, datetime, timedelta
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from home.models import FoodItems, MealNutrients, NutrientsTracking

# Create your views here.


def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    items = FoodItems.objects.filter(username=request.user.username)
    return render(request, "index.html", {"items": items})


def addFoodItems(request):
    if request.method == 'POST':
        username = request.user.username
        name = request.POST['name']
        calorie = request.POST['calorie']
        protein = request.POST['protein']
        fat = request.POST['fat']
        if len(request.FILES) != 0:
            image = request.FILES['image']
        item = FoodItems(username=username, name=name, calorie=calorie,
                         protein=protein, fat=fat, image=image)
        item.save()
        messages.success(request, "Data submitted successfully")
    return HttpResponseRedirect("/")


def loginUser(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.warning(request, "Incorrect username or password")
            return render(request, "login.html")
    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(name, email, password)
        user.save()
        messages.success(request, "User registered successfully")

    return render(request, "signup.html")


def logoutUser(request):
    logout(request)
    return redirect("/login")


def addToFavorites(request, id):
    item = get_object_or_404(FoodItems, id=id)
    if item.favorite.filter(id=request.user.id).exists():
        pass
    else:
        item.favorite.add(request.user)
        messages.success(request, "Added to favorites")
    return redirect("/")


def favorites(request):
    user = request.user
    favorite = user.favorite.all()
    return render(request, "favorites.html", {"favorite": favorite})


def trackingMealNutrients(request):
    if request.method == "POST":
        username = request.user.username
        meal = request.POST['meal']
        calorie = request.POST['calorie']
        protein = request.POST['protein']
        fat = request.POST['fat']
        fiber = request.POST['fiber']
        meal = MealNutrients(username=username, meal=meal, calorie=calorie,
                             protein=protein, fat=fat, fiber=fiber)
        meal.save()
    return HttpResponseRedirect("/trackingNutrients")


def trackingNutrients(request):
    meals = MealNutrients.objects.filter(
        username=request.user.username,
        day=date.today())
    return render(request, "trackingNutrients.html", {"meals": meals})


def weekly(request):
    items = MealNutrients.objects.filter(username=request.user.username,
                                         day=date.today())
    calorie = 0
    protein = 0
    fat = 0
    fiber = 0
    for item in items:
        calorie = calorie + item.calorie
        protein = protein + item.protein
        fat = fat + item.fat
        fiber = fiber + item.fiber
    if NutrientsTracking.objects.filter(username=request.user.username,
                                        date=date.today()).exists():
        meal = NutrientsTracking.objects.get(username=request.user.username,
                                             date=date.today())
        meal.calorie = calorie
        meal.protein = protein
        meal.fat = fat
        meal.fiber = fiber
        meal.save()
    else:
        meal = NutrientsTracking(username=request.user.username,
                                 calorie=calorie, protein=protein, fat=fat, fiber=fiber)
        meal.save()
    re = NutrientsTracking.objects.get(username=request.user.username,
                                       date=date.today())
    if re.day <= 7:
        records = NutrientsTracking.objects.filter(
            username=request.user.username)[:re.day+1]
    else:
        x = re.day - 7
        records = NutrientsTracking.objects.filter(
            username=request.user.username)[x:re.day+1]

    return render(request, "weekly.html", {"records": records})


def monthly(request):
    items = MealNutrients.objects.filter(username=request.user.username,
                                         day=date.today())
    calorie = 0
    protein = 0
    fat = 0
    fiber = 0
    for item in items:
        calorie = calorie + item.calorie
        protein = protein + item.protein
        fat = fat + item.fat
        fiber = fiber + item.fiber
    if NutrientsTracking.objects.filter(username=request.user.username,
                                        date=date.today()).exists():
        meal = NutrientsTracking.objects.get(username=request.user.username,
                                             date=date.today())
        meal.calorie = calorie
        meal.protein = protein
        meal.fat = fat
        meal.fiber = fiber
        meal.save()
    else:
        meal = NutrientsTracking(username=request.user.username,
                                 calorie=calorie, protein=protein, fat=fat, fiber=fiber)
        meal.save()
    re = NutrientsTracking.objects.get(username=request.user.username,
                                       date=date.today())
    if re.day <= 30:
        records = NutrientsTracking.objects.filter(
            username=request.user.username)[:re.day+1]
    else:
        x = re.day - 30
        records = NutrientsTracking.objects.filter(
            username=request.user.username)[x:re.day+1]

    return render(request, "monthly.html", {"records": records})


# def workout(request):
#     return render(request, "workout.html")


# def notify(request):
#     hr = ToastNotifier()
#     hr.show_toast("alert", "A new notification")
#     return HttpResponseRedirect("/workout")
