from win10toast import ToastNotifier
from datetime import date, datetime, timedelta
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from home.models import FoodItems, MealNutrients

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
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = some_day_last_week - \
        timedelta(days=(some_day_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)
    meals = MealNutrients.objects.filter(created_at__gte=monday_of_last_week,
                                         created_at__lt=monday_of_this_week)
    print(meals)
    return HttpResponseRedirect("trackingNutrients")


def workout(request):
    return render(request, "workout.html")

def notify(request):
    hr = ToastNotifier()
    hr.show_toast("alert", "A new notification")
    return HttpResponseRedirect("/workout")
