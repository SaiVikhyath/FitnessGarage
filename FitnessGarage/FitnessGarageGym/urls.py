from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register.html', views.register),
    path('dashboard.html', views.dashboard)
]