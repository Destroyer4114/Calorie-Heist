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
]
