from django.db import models
from django.contrib.auth.models import User
import json

# Assuming you have the Team and Subteam models in the teams app
from teams.models import Team, Subteam

class Schedule(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    subteam = models.ForeignKey(Subteam, on_delete=models.SET_NULL, null=True)
    schedule_data = models.TextField()  # Keeping the same schedule field

    def save(self, *args, **kwargs):
        self.schedule_data = json.dumps(self.schedule_data)
        super(Schedule, self).save(*args, **kwargs)

    @property
    def get_schedule_data(self):
        return json.loads(self.schedule_data)

    def __str__(self):
        return f"{self.user.username}'s schedule"
