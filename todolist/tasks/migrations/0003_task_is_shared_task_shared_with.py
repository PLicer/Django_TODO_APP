# Generated by Django 5.1.1 on 2024-09-21 06:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_shared',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
