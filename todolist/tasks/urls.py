from tkinter.font import names

from django.urls import path
from .import views

urlpatterns=[
    path('tasks/',views.task_list,name='task_list'),
    path('tasks/add/',views.add_task,name='add_task'),
    path('tasks/<int:pk>/',views.task_details,name='task_details'),
    path('tasks/<int:pk>/update/',views.update_task,name='update_task'),
    path('tasks/<int:pk>/delete/',views.delete_task,name='delete_task'),
    path('tasks/<int:task_pk>/subtasks/add/',views.add_subtask,name='add_subtask'),
    path('tasks/<int:task_pk>/subtasks/<int:subtask_pk>/update/',views.updated_subtask,name='update_subtask'),
    path('tasks/<int:task_pk>/subtasks/<int:subtask_pk>/delete/',views.delete_subtask,name='delete_subtask'),
    path('tasks/<int:pk>/subtasks/get/',views.subtask_list,name='subtask_list'),
    path('register/',views.register,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('tasks/share/<int:task_id>/<int:recipient_user_id>/',views.share_task,name='share_task'),
    path('tasks/shared/',views.view_shared_tasks,name='view_shared_tasks')
]