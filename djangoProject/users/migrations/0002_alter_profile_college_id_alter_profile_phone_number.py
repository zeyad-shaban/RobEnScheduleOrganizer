# Generated by Django 5.1.1 on 2024-09-27 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="college_id",
            field=models.CharField(blank=True, max_length=9, unique=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="phone_number",
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
    ]
