from django.urls import path
from core import views

urlpatterns = [
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('register/', views.register, name='register'),

    path('user/', views.get_user, name='get_user'),
    path('user/set-image', views.set_image, name='set_image'),
    path('user/edit', views.edit_user, name='edit_user'),
    path('user/change-password', views.edit_user_password, name='edit_user_password'),
] 