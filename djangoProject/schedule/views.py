import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Schedule
from teams.models import Team, Subteam
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required(login_url='/users/login/')
def save_schedule(request):
    if request.method == 'POST':
        schedule_data = json.loads(request.body.decode('utf-8'))
        schedule_data = schedule_data.get('schedule_data')

        schedule, created = Schedule.objects.get_or_create(user=request.user)
        schedule.schedule_data = schedule_data  # Update with new 2D array
        schedule.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def staff_or_superuser(user):
    return user.is_staff or user.is_superuser


# THERE ARE MANY HARDCODED VALUES HERE REGARDING THE SCHEDULE
@user_passes_test(staff_or_superuser, login_url='/users/login/')
def team_schedule(request):
    team_id = request.GET.get('team')
    subteam_id = request.GET.get('subteam')

    if team_id and subteam_id:
        team = get_object_or_404(Team, id=team_id)
        subteam = get_object_or_404(Subteam, id=subteam_id, team=team)
        users = User.objects.filter(schedule__team=team, schedule__subteam=subteam)
    else:
        schedule = Schedule.objects.get_or_create_for_user(request.user)
        team = schedule.team
        subteam = schedule.subteam
        users = User.objects.filter(schedule__team=team, schedule__subteam=subteam) if team and subteam else []

    total_schedule = [[0 for _ in range(7)] for _ in range(6)]  # For counting busy users
    user_busy_tracker = [[[] for _ in range(7)] for _ in range(6)]  # For tracking busy users

    for user in users:
        schedule = Schedule.objects.get_or_create_for_user(user)
        schedule_data = schedule.get_schedule_data

        for i in range(6):
            for j in range(7):
                if schedule_data[i][j] == 1:
                    total_schedule[i][j] += 1
                    user_busy_tracker[i][j].append(
                        f'{user.username} - {user.first_name} {user.last_name} - ID: {user.profile.college_id} - No.: {user.profile.phone_number} [{"New" if user.profile.new_member else "Old"} Member]'
                    )

    return render(request, 'schedule/team_schedule.html', {
        'schedule': total_schedule,
        'user_busy_tracker': user_busy_tracker,
        'cols_range': ['8:30->10:30', '10:30->12:30', '12:30->2:30', '2:30->4:30', '4:30->6:30', '6:30->8:30', '8:30->10:30'],
        'team': team,
        'subteam': subteam,
        'teams': Team.objects.all(),
        'subteams': Subteam.objects.all()
    })

def get_subteams(request):
    team_id = request.GET.get('team_id')
    subteams = Subteam.objects.filter(team_id=team_id).values('id', 'name')
    return JsonResponse({'subteams': list(subteams)})