from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from home.models import FoodItems

# Create your views here.


def index(request):
    if request.user.is_anonymous:
        return redirect("/login")

    if request.method == 'POST':
        name = request.POST['name']
        calorie = request.POST['calorie']
        protein = request.POST['protein']
        fat = request.POST['fat']
        if len(request.FILES) != 0:
            image = request.FILES['image']
        item = FoodItems(name=name, calorie=calorie,
                         protein=protein, fat=fat, image=image)
        item.save()
        messages.success(request, "Data submitted successfully")
    items = FoodItems.objects.all()
    return render(request, "index.html", {"items": items})


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
