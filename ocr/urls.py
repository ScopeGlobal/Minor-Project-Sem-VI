from atexit import register
from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("dashboard",views.dashboardpage, name="dashboard"),
    re_path('^register$', views.registerpage, name="register"),
    re_path('^login$', views.loginpage, name="login"),
    path('logout',views.logoutUser,name='logout'), 
    re_path(r'profile/(?P<username>.+)/$', views.profile, name="profile"),
    re_path(r'basepage/(?P<username>.+)/$', views.basepage, name="base"),    
]
