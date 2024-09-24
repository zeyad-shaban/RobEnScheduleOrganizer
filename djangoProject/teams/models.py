from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Subteam(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='subteams')

    class Meta:
        unique_together = ('name', 'team')

    def __str__(self):
        return f'{self.name} ({self.team.name})'