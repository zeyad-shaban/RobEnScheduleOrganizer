from django.shortcuts import render
from django.shortcuts import render, redirect
from schedule.models import Schedule
import json
from django.contrib.auth.decorators import login_required


@login_required(login_url='/users/login/')
def home(request):
    schedule = Schedule.objects.get_or_create_for_user(request.user)
    schedule_data = schedule.get_schedule_data

    return render(request, 'home.html', {
        'schedule': schedule_data,
        'cols_range': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'],
        'days_list': "Sat Sun Mon Tue Wed Thu".split(" ")
    })