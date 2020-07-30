from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random_page", views.random_page, name="random_page"),
    path("add", views.add, name="add"),
    path("wiki/<str:title>", views.wiki_page, name="wiki_page"),
    path("search", views.search, name="search"),
    path("wiki/edit/<str:title>", views.edit, name="edit")
]
