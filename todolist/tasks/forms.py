from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task,Subtask


class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model =User
        fields=['username','email','password1','password2']


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)


class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description']

class SubtaskForm(forms.ModelForm):
    class Meta:
        model=Subtask
        fields=['title','is_completed']

class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title','description']

class UpdateSubtaskForm(forms.ModelForm):
    class Meta:
        model=Subtask
        fields=['title','is_completed']
