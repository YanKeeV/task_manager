from django.urls import path
from manager import views

urlpatterns = [
    path('<str:project>', views.get_project, name='get_project'),
    path('projects/<str:status>', views.project_list_by_user, name='project_list'),
    path('<int:project>/tasks', views.task_list_by_project, name='task_list_by_project'),
    path('project/create', views.create_project, name='project_create'),
    path('project/edit', views.edit_project, name='project_edit'),
    path('<int:project>/users', views.users_by_project, name='users_by_project'),
    path('<int:project>/users/archive', views.users_by_project_for_archive, name='users_by_project_for_archive'),
    path('project/add/user', views.user_to_project, name='user_to_project'),
    path('project/delete', views.delete_project, name='delete_project'),
    path('project/delete/user', views.delete_user_from_project, name='delete_user_from_project'),
    path('project/finish', views.finish_project, name='finish_project'),

    path('project/invites/', views.get_project_invites, name='get_project_invites'),
    path('project/invite/create', views.create_project_invite, name='create_project_invite'),
    path('project/invite/accept', views.accept_project_invite, name='accept_project_invite'),
    path('project/invite/decline', views.decline_project_invite, name='decline_project_invite'),

    path('tasks/', views.task_list_by_user, name='task_list'),
    path('task/create', views.create_task, name='task_create'),
    path('task/edit', views.edit_task, name='task_edit'),
    path('task/status', views.task_status, name='task_status'),
    path('task/add/user', views.user_to_task, name='user_to_task'),
    path('task/delete', views.delete_task, name='delete_task'),
    path('task/delete/user', views.delete_user_from_task, name='delete_user_from_task'),

    path('teams/', views.team_list_by_user, name='team_list_by_user'),
    path('team/create', views.create_team, name='create_team'),
    path('team/<int:team>/users', views.users_by_team, name='users_by_team'),
    path('team/delete/user', views.delete_user_from_team, name='delete_user_from_team'),
    path('team/<int:team>/tasks', views.task_list_by_team, name='task_list_by_team'),

    path('team/invites/', views.get_team_invites, name='get_team_invites'),
    path('team/invite/create', views.create_team_invite, name='create_team_invite'),
    path('team/invite/accept', views.accept_team_invite, name='accept_team_invite'),
    path('team/invite/decline', views.decline_team_invite, name='deciline_team_invite'),

    path('permissions/<int:project>/<str:user>', views.get_user_permissions, name='get_user_permissions'),
    path('permissions/edit', views.edit_permission, name='edit_permission'),

    path('comment/get/<int:task>', views.get_comments, name='get_comments'),
    path('comment/create', views.create_comment, name='create_comment'),
    path('comment/delete/<int:id>', views.delete_comment, name='delete_comment'),
]