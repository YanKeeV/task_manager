from django.urls import path
from core import views

urlpatterns = [
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('register/', views.register, name='register'),

    path('user/', views.get_user, name='get_user'),
    path('user/edit', views.edit_user, name='edit_user'),
    #path('user/<int:project>/tasks', views.task_list_by_user_and_project, name='task_list_by_user_and_project'),
]