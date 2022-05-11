from atexit import register
from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    re_path('^register$', views.register, name="register"),
    re_path('^login$', views.login, name="login"),
]
