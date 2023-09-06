from django.urls import path
from manager import views

urlpatterns = [
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('register/', views.register, name='register'),

    path('user/', views.get_user, name='get_user'),
    path('user/edit', views.edit_user, name='edit_user'),
    path('user/<int:project>/tasks', views.task_list_by_user_and_project, name='task_list_by_user_and_project'),
    
    path('<str:project>', views.get_project, name='get_project'),
    path('projects/', views.project_list_by_user, name='project_list'),
    path('<int:project>/tasks', views.task_list_by_project, name='task_list_by_project'),
    path('project/create', views.create_project, name='project_create'),
    path('project/edit', views.edit_project, name='project_edit'),
    path('<int:project>/users', views.users_by_project, name='users_by_project'),
    path('project/add/user', views.user_to_project, name='user_to_project'),
    path('project/delete', views.delete_project, name='delete_project'),
    path('project/delete/user', views.delete_user_from_project, name='delete_user_from_project'),
    path('project/finish', views.finish_project, name='finish_project'),

    path('tasks/', views.task_list_by_user, name='task_list'),
    path('task/create', views.create_task, name='task_create'),
    path('task/edit', views.edit_task, name='task_edit'),
    path('task/status', views.task_status, name='task_status'),
    path('task/add/user', views.user_to_task, name='user_to_task'),
    path('task/delete', views.delete_task, name='delete_task'),
    path('task/delete/user', views.delete_user_from_task, name='delete_user_from_task'),
]