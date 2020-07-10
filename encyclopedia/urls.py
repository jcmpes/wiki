from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<title>", views.entry, name="entry")
]
