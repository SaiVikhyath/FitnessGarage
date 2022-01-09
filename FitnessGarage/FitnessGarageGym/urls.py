from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register.html', views.register),
    path('dashboard.html', views.dashboard),
    path('personalTraining.html', views.personalTraining),
    path('cardioMembers.html', views.cardioMembers),
    path('weightsMembers.html', views.weightsMembers),
    path('allMembers.html', views.allMembers)
]