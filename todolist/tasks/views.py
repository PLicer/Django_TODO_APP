from django.shortcuts import get_object_or_404,redirect
from django.http import JsonResponse
from django.template.context_processors import request

from .models import Task,Subtask
from .forms import TaskForm,SubtaskForm,UpdateTaskForm,UpdateSubtaskForm,UserLoginForm,UserRegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@csrf_exempt
def register (request):
    if request.method =="POST":
        import json
        data=json.loads(request.body)
        form = UserRegisterForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'message':'User registered successfully'})
        return JsonResponse({'error':form.errors},status=400)
    return JsonResponse({'error':'Invalid request'},status=400)

@csrf_exempt
def login_user(request):
    if request.method =='POST':
        import json
        data=json.loads(request.body)
        form = UserLoginForm(data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message':'Logged in successfully'})
            else:
                return JsonResponse({'error':'Invalid credentials'},status=400)
        return JsonResponse({'error':form.errors},status=400)
    return JsonResponse({'error':'Invalid request'},status=400)


@csrf_exempt
@login_required
def logout_user(request):
    logout(request)
    return JsonResponse({'message':'Logged out successfully'})


@login_required
def task_list(request):
    tasks=Task.objects.filter(user=request.user)
    tasks_data=[
        {
            'id':task.id,
            'title':task.title,
            'description':task.description,
            'created_at':task.created_at,
            'updated_at':task.updated_at

        }
        for task in tasks
    ]
    return JsonResponse(tasks_data,safe=False)

@csrf_exempt
@login_required
def add_task(request):

    if request.method=='POST':
        import json
        data = json.loads(request.body)
        form=TaskForm(data)
        if form.is_valid():
            task=form.save(commit=False)
            task.user=request.user
            task.save()
            task_data={
                'id':task.id,
                'title':task.title,
                'description':task.description,
                'created_at':task.created_at,
                'updated_at':task.updated_at
            }
            return JsonResponse(task_data,status=201)
    return JsonResponse({'error':'Invalid request'},status=400)

@login_required
def task_details(request,pk):
    task = Task.objects.filter(pk=pk,user=request.user).first()
    if not task:
        return JsonResponse({'error': 'Task not found with the given ID'}, status=404)
    # task=get_object_or_404(Task,pk=pk)
    subtasks=Subtask.objects.filter(task=task)
    subtasks_data=[
        {
            'id':subtask.id,
            'title':subtask.title,
            'is_completed':subtask.is_completed,
            'created_at':subtask.created_at,
            'updated_at':subtask.updated_at
        }
        for subtask in subtasks
    ]
    task_data={
        'id':task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at,
        'updated_at': task.updated_at,
        'subtasks':subtasks_data
    }
    return JsonResponse(task_data)

@csrf_exempt
@login_required
def update_task(request,pk):
    if request.method=='PUT':
        task = Task.objects.filter(pk=pk,user=request.user).first()
        if not task:
            return JsonResponse({'error': 'Task not found with the given ID'}, status=404)
        import json
        data=json.loads(request.body)
        form=UpdateTaskForm(data,instance=task)
        if form.is_valid():
            task=form.save()
            task_data={
                'id':task.id,
                'title':task.title,
                'description':task.description,
                'created_at':task.created_at,
                'updated_at':task.updated_at
            }
            return JsonResponse(task_data)
    return JsonResponse({'error':'Invalid request'},status=400)

@csrf_exempt
@login_required
def delete_task(request,pk):
    if request.method == 'DELETE':
        task = Task.objects.filter(pk=pk,user=request.user).first()
        if not task:
            return JsonResponse({'error': 'Task not found with the given ID'}, status=404)
        task.delete()
        return JsonResponse({'message':'Task deleted successfully'})
    return JsonResponse({'error':'Invalid request'},status=400)

@csrf_exempt
@login_required
def add_subtask(request,task_pk):

    if request.method =='POST':
        task = Task.objects.filter(pk=task_pk,user=request.user).first()
        if not task:
            return JsonResponse({'error': 'Task not found with the given ID'}, status=404)
        import json
        data = json.loads(request.body)
        form=SubtaskForm(data)
        if form.is_valid():
            subtask=form.save(commit=False)
            subtask.task=task
            subtask.save()
            subtask_data={
                'id':subtask.id,
                'title':subtask.title,
                'is_completed':subtask.is_completed,
                'created_at':subtask.created_at,
                'updated_at':subtask.updated_at
            }
            return JsonResponse(subtask_data)
        return JsonResponse({'error':'Invalid request'},status=400)

@csrf_exempt
@login_required
def updated_subtask(request,task_pk,subtask_pk):

    if request.method == 'PUT':
        task = Task.objects.filter(pk=task_pk,user=request.user).first()
        if not task:
            return JsonResponse({'error': 'Task not found with the given ID'}, status=404)
        subtask = Subtask.objects.filter(pk=subtask_pk,task=task).first()
        if not subtask:
            return JsonResponse({'error': 'SubTask not found with the given ID'}, status=404)
        import json
        data=json.loads(request.body)
        form=UpdateSubtaskForm(data,instance=subtask)
        if form.is_valid():
            subtask=form.save()
            subtask_data={
                'id':subtask.id,
                'title':subtask.title,
                'is_completed':subtask.is_completed,
                'created_at':subtask.created_at,
                'updated_at':subtask.updated_at
            }
            return JsonResponse(subtask_data)
        return JsonResponse({'error':'Invalid request'},status=400)

@csrf_exempt
@login_required
def delete_subtask(request,task_pk,subtask_pk):

    if request.method == 'DELETE':
        task = Task.objects.filter(pk=task_pk,user=request.user).first()
        if not task:
            return JsonResponse({'error': 'Task not found with the given ID'}, status=404)
        subtask = Subtask.objects.filter(pk=subtask_pk,task=task).first()
        if not subtask:
            return JsonResponse({'error': 'SubTask not found with the given ID'}, status=404)
        subtask.delete()
        return JsonResponse({'message':'Subtask deleted successfully'})
    return JsonResponse({'error':'Invalid request'},status=400)


@login_required
def subtask_list(request,pk):
    task = Task.objects.filter(pk=pk,user=request.user).first()
    if not task:
        return JsonResponse({'error': 'Task not found with the given ID'}, status=404)
    subtasks = Subtask.objects.filter(task=task)
    subtasks_data=[
        {
            'id':subtask.id,
            'title':subtask.title,
            'is_completed':subtask.is_completed,
            'created_at':subtask.created_at,
            'updated_at':subtask.updated_at

        }
        for subtask in subtasks
    ]
    return JsonResponse(subtasks_data,safe=False)
