from django.shortcuts import render
from django.shortcuts import render, redirect
from schedule.models import Schedule
import json
from django.contrib.auth.decorators import login_required


@login_required(login_url='/users/login/')
def home(request):
    schedule = Schedule.objects.get_or_create_for_user(request.user)
    schedule_data = schedule.get_schedule_data
    team = schedule.team
    subteam = schedule.subteam

    return render(request, 'home.html', {
        'schedule': schedule_data,
        'team': team,
        'subteam': subteam,
        'cols_range': ['8:30->10:30', '10:30->12:30', '12:30->2:30', '2:30->4:30', '4:30->6:30', '6:30->8:30', '8:30->10:30'],
        'days_list': "Sat Sun Mon Tue Wed Thu".split(" "),
    })
