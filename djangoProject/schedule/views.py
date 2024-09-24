import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Schedule
from django.contrib.auth.models import User

def save_schedule(request):
    if request.method == 'POST':
        schedule_data = json.loads(request.body.decode('utf-8'))
        schedule_data = schedule_data.get('schedule_data')

        schedule, created = Schedule.objects.get_or_create(user=request.user)
        schedule.schedule_data = schedule_data  # Update with new 2D array
        schedule.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def team_schedule(request):
    users = User.objects.all()
    total_schedule = [[0 for _ in range(16)] for _ in range(6)]  # For counting busy users
    user_busy_tracker = [[[] for _ in range(16)] for _ in range(6)]  # For tracking busy users

    for user in users:
        try:
            schedule = Schedule.objects.get(user=user)
            schedule_data = json.loads(schedule.schedule_data)
            # Summing schedules and tracking who is busy
            for i in range(6):  # Iterate through rows
                for j in range(16):  # Iterate through columns
                    if schedule_data[i][j] == 1:
                        total_schedule[i][j] += 1
                        user_busy_tracker[i][j].append(f'{user.first_name} {user.last_name}')
        except Schedule.DoesNotExist:
            continue  # Skip users without a schedule

    return render(request, 'schedule/team_schedule.html', {
        'schedule': total_schedule,  # Pass the count schedule
        'user_busy_tracker': user_busy_tracker,  # Pass the busy users
        'cols_range': range(1, 17),
    })