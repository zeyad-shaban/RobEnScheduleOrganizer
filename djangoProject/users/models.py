from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college_id = models.CharField(max_length=9, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    new_member = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username