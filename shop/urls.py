from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about", views.about, name="about me"),
    path("tracker",views.tracker, name="mytracker"),
    path("contact",views.contact, name="contact"),
    path("products/<int:myid>",views.prodview,name="prodview"),
    path("checkout",views.checkout),
    path("search/",views.search)
]