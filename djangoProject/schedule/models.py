# users/models.py
from django.db import models
from django.contrib.auth.models import User
import json
from teams.models import Team, Subteam

class ScheduleManager(models.Manager):
    def get_or_create_for_user(self, user):
        try:
            return self.get(user=user)
        except Schedule.DoesNotExist:
            # If schedule doesn't exist, create it with default values
            initial_schedule = [[0 for _ in range(14)] for _ in range(6)]
            return self.create(user=user, schedule_data=json.dumps(initial_schedule))

class Schedule(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    subteam = models.ForeignKey(Subteam, on_delete=models.SET_NULL, null=True)
    schedule_data = models.TextField()  # Keeping the same schedule field

    # Attach the custom manager
    objects = ScheduleManager()

    def save(self, *args, **kwargs):
        if isinstance(self.schedule_data, list):
            self.schedule_data = json.dumps(self.schedule_data)
        super(Schedule, self).save(*args, **kwargs)

    @property
    def get_schedule_data(self):
        return json.loads(self.schedule_data)

    def __str__(self):
        return f"{self.user.username}'s schedule"
