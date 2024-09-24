from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('settings/', views.settings_view, name='settings'),

    path('settings/update_team_subteam/', views.update_team_subteam, name='update_team_subteam'),
    path('settings/update_user_details/', views.update_user_details, name='update_user_details'),
    path('settings/change_password/', views.change_password, name='change_password'),

]