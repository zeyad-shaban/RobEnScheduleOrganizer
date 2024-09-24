from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('save/', views.save_schedule, name='save_schedule'),
    path('team/', views.team_schedule, name='team_schedule'),
]