from datetime import date, datetime, timedelta
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from home.models import Notifications

from home.models import FoodItems, MealNutrients, NutrientsTracking

# Create your views here.


def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    items = FoodItems.objects.filter(username=request.user.username)
    print(str(datetime.now().hour) + ":" + str(datetime.now().minute))
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


def calorieNeed(request):
    return render(request, "calorieNeed.html")


def calorieCalculator(request):
    if request.method == "POST":
        height = request.POST['height']
        weight = request.POST['weight']
        age = request.POST['age']
        gender = request.POST['gender']
        activity = request.POST['activity']
        bmr = 0
        bmi = float(weight)/(float(height)*float(height))
        bmi = bmi*10000
        bmi = round(bmi, 2)
        if gender == "male":
            bmr = 5 + (10*float(weight)) + \
                (6.25*float(height)) - (5*float(age))
        elif gender == "female":
            bmr = (10*float(weight)) + \
                (6.25*float(height)) - (5*float(age)) - 161
        calorie = 0
        if activity == "sedentary":
            calorie = bmr*1.2
        elif activity == "light":
            calorie = bmr*1.375
        elif activity == "moderate":
            calorie = bmr*1.55
        elif activity == "very":
            calorie = bmr*1.725
        elif activity == "extra":
            calorie = bmr*1.9

    protein = calorie/5
    fat = calorie/4
    carbohydrate = calorie - (protein+fat)
    protein /= 4
    fat /= 9
    carbohydrate /= 4
    protein = round(protein, 2)
    fat = round(fat, 2)
    carbohydrate = round(carbohydrate, 2)
    calorie = round(calorie, 2)
    context = {"calorie": calorie, "bmi": bmi,
               "carbohydrate": carbohydrate, "protein": protein, "fat": fat}
    return render(request, "calorieNeed.html", context)


def healthTip(request):
    return render(request, "healthTip.html")


def portfolio(request):
    records = MealNutrients.objects.filter(
        username=request.user.username, day=date.today())
    calorie = 0
    protein = 0
    fat = 0
    fiber = 0
    for record in records:
        calorie += record.calorie
        protein += record.protein
        fat += record.fat
        fiber += record.fiber
    context = {
        "calorie": calorie,
        "protein": protein,
        "fat": fat,
        "fiber": fiber
    }
    return render(request, "portfolio.html", context)


def workout(request):
    return render(request, "workoutTracker.html")


def activitySelection(request):
    if request.method == "POST":
        height = request.POST['height']
        weight = request.POST['weight']
        age = request.POST['age']
        gender = request.POST['gender']
        duration = request.POST['duration']
        speed = request.POST['speed']
        bmr = 0
        if gender == "male":
            bmr = 5 + (10*float(weight)) + \
                (6.25*float(height)) - (5*float(age))
        elif gender == "female":
            bmr = (10*float(weight)) + \
                (6.25*float(height)) - (5*float(age)) - 161
        mets = float(speed)*(float(duration)/60)
        calorie = (bmr*mets)/24
        return render(request, "workoutTracker.html", {"calorie": calorie, "bmr": bmr})
