from django.db import migrations, models
import json

def add_default_schedule(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Schedule = apps.get_model('schedule', 'Schedule')
    default_schedule = json.dumps([[0] * 16 for _ in range(6)])

    for user in User.objects.all():
        if not Schedule.objects.filter(user=user).exists():
            Schedule.objects.create(user=user, schedule_data=default_schedule)

class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),  # Ensure this matches the name of your initial migration file
    ]

    operations = [
        migrations.RunPython(add_default_schedule),
    ]
