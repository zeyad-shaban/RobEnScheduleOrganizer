from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Schedule

@receiver(post_save, sender=User)
def create_schedule(sender, instance, created, **kwargs):
    if created:
        initial_schedule = [[0 for _ in range(16)] for _ in range(6)]
        Schedule.objects.create(user=instance, schedule_data=initial_schedule)