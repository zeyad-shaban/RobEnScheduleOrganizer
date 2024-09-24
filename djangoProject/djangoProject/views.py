from django.shortcuts import render
from django.shortcuts import render, redirect
from schedule.models import Schedule
import json
from django.contrib.auth.decorators import login_required


@login_required(login_url='/users/login/')
def home(request):
    if request.user.is_authenticated:
        try:
            schedule = Schedule.objects.get(user=request.user)
            # Make sure schedule_data is interpreted as a list
            schedule_data = json.loads(schedule.schedule_data) if isinstance(schedule.schedule_data,
                                                                             str) else schedule.schedule_data
        except Schedule.DoesNotExist:
            initial_schedule = [[0 for _ in range(14)] for _ in range(6)]
            schedule = Schedule.objects.create(user=request.user, schedule_data=initial_schedule)
            schedule_data = initial_schedule

        return render(request, 'home.html', {
            'schedule': schedule_data,
            'cols_range': range(1, 15),
            'days_list': "Sat Sun Mon Tue Wed Thu".split(" ")
        })
    else:
        return redirect('users/login')
