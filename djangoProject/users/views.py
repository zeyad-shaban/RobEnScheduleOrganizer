from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from schedule.models import Team, Subteam
from django.http import JsonResponse
from schedule.models import Schedule
from .forms import UserUpdateForm, CustomPasswordChangeForm, CustomUserCreationForm
from .models import Profile
from django.db import IntegrityError


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
            user = form.save()  # Save the user first
            try:
                team = form.cleaned_data.get('team')
                subteam = form.cleaned_data.get('subteam')
                college_id = form.cleaned_data.get('college_id')
                email = form.cleaned_data.get('email')
                phone_number = form.cleaned_data.get('phone_number')
                new_member = form.cleaned_data.get('new_member')

                # Save extra fields in the profile
                user.email = email
                user.save()

                # Get or create the Profile instance
                profile, created = Profile.objects.get_or_create(user=user)
                profile.college_id = college_id
                profile.phone_number = phone_number
                profile.new_member = new_member
                profile.save()

                # Save schedule and team information
                schedule = Schedule.objects.get_or_create_for_user(user)
                schedule.team = team
                schedule.subteam = subteam
                schedule.schedule_data = [[0 for _ in range(14)] for _ in range(6)]  # Initial schedule data
                schedule.save()

                login(request, user)  # Log in the user
                messages.success(request, 'Account created successfully.')
                return JsonResponse({'success': True, 'message': 'Account created successfully.'})
            except IntegrityError as e:
                user.delete()  # Delete the user if profile creation fails
                form.add_error(None, ValidationError(str(e)))
                errors = form.errors.as_json()
                return JsonResponse({'success': False, 'errors': errors})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = CustomUserCreationForm()
    teams = Team.objects.all()
    subteams = Subteam.objects.all()
    return render(request, 'users/signup.html', {'form': form, 'teams': teams, 'subteams': subteams})
@login_required(login_url='/users/login/')
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


@login_required(login_url='/users/login/')
def update_team_subteam(request):
    if request.method == 'POST':
        team_id = request.POST.get('team')
        subteam_id = request.POST.get('subteam')
        user = request.user

        # Use get_or_create to avoid manually handling the DoesNotExist exception
        schedule, created = Schedule.objects.get_or_create(user=user)

        # Update the team and subteam
        schedule.team_id = team_id
        schedule.subteam_id = subteam_id
        schedule.save()

        return JsonResponse({'success': True, 'message': 'Team and Subteam updated successfully.'})


@login_required(login_url='/users/login/')
def update_user_details(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user = user_form.save()

            # Update profile fields
            profile, created = Profile.objects.get_or_create(user=user)
            profile.college_id = user_form.cleaned_data['college_id']
            profile.phone_number = user_form.cleaned_data['phone_number']
            profile.new_member = user_form.cleaned_data['new_member']
            profile.save()

            messages.success(request, 'User details updated successfully.')
            return JsonResponse({'success': True})

        errors = user_form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})

@login_required(login_url='/users/login/')
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
