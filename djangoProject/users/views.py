from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import UserUpdateForm, CustomPasswordChangeForm, CustomUserCreationForm
from schedule.models import Team, Subteam
from django.http import JsonResponse
from schedule.models import Schedule

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return JsonResponse({'success': True, 'message': 'Account created successfully.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = CustomUserCreationForm()
    teams = Team.objects.all()
    subteams = Subteam.objects.all()
    return render(request, 'users/signup.html', {'form': form, 'teams': teams, 'subteams': subteams})

@login_required
def settings_view(request):
    user = request.user
    user_form = UserUpdateForm(instance=user)
    password_form = CustomPasswordChangeForm(user)
    teams = Team.objects.all()
    subteams = Subteam.objects.all()

    return render(request, 'users/settings.html', {
        'user_form': user_form,
        'password_form': password_form,
        'teams': teams,
        'subteams': subteams,
        'current_team': user.schedule.team if hasattr(user, 'schedule') else None,
        'current_subteam': user.schedule.subteam if hasattr(user, 'schedule') else None,
    })

@login_required
def update_team_subteam(request):
    if request.method == 'POST':
        team_id = request.POST.get('team')
        subteam_id = request.POST.get('subteam')
        user = request.user

        try:
            schedule = Schedule.objects.get(user=user)
        except Schedule.DoesNotExist:
            initial_schedule = [[0 for _ in range(16)] for _ in range(6)]
            schedule = Schedule.objects.create(user=user, schedule_data=initial_schedule)

        schedule.team_id = team_id
        schedule.subteam_id = subteam_id
        schedule.save()
        return JsonResponse({'success': True, 'message': 'Team and Subteam updated successfully.'})


@login_required
def update_user_details(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'User details updated successfully.')
            return JsonResponse({'success': True})

        errors = user_form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})

@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keep user logged in after password change
            return JsonResponse({'success': True, 'message': 'Password changed successfully.'})
        else:
            errors = password_form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})

