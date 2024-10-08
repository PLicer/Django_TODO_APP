from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_shared = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(User,related_name='shared_tasks',blank=True)

    def __str__(self):
        return self.title

class Subtask(models.Model):
    task=models.ForeignKey(Task,related_name='subtasks',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title