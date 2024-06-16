from django.urls import path
from storage import views

urlpatterns = [
    path('files/', views.register, name='register'),
]