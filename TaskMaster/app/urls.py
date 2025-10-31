# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('app/home', views.home_view, name='home'),
    path('app/all_tasks', views.all_tasks, name='all_tasks'),
    path('app/expired_tasks', views.expired_tasks, name='expired_tasks'),
    path('app/completed_tasks', views.completed_tasks, name='completed_tasks'),
    path('app/pending_tasks', views.pending_tasks, name='pending_tasks'),
    path('create/', views.task_create, name='task_create'),
    path('update/<int:pk>/', views.task_update, name='task_update'),
    path('update_status/<int:pk>/', views.update_status, name='update_status'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_view, name='register'),
]

