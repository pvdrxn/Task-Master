# tasks/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from datetime import datetime

from .models import Task
from .forms import TaskForm

# Registro de usuarios
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            messages.success(request, f'Cuenta creada para {username}!')

            authenticated_user = authenticate(username=username, password=raw_password)
            if authenticated_user is not None:
                login(request, authenticated_user) 
                return redirect('task_list')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form })
                                                
# Inicio de sesión
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def home_view(request):
    all_tasks = Task.objects.all()
    pendientes = Task.objects.filter(
        completed=False
    ).filter(
        Q(due_date__gte=timezone.now()) | Q(due_date__isnull=True)
    ).count()

    completadas = Task.objects.filter(completed=True).count()
    expiradas = Task.objects.filter(due_date__lt=timezone.now(), completed=False).count()

    context = {
        'total': all_tasks.count(),
        'completadas': completadas,
        'pendientes': pendientes,
        'expiradas': expiradas,
    }

    return render(request, 'home.html', context)

# Cerrar sesión
def logout_user(request):
    logout(request)
    return redirect('login')

# Vista para listar todas las tareas
@login_required
def all_tasks(request):
    tasks = Task.objects.filter(user=request.user)

    if not tasks:
        messages.warning(request, 'No hay tareas por el momento...')
    else:
        # Ordenar las tareas: primero las pendientes, luego las completadas y manejar due_date opcional
        tasks = sorted(tasks, key=lambda x: (x.completed, x.due_date.date() if x.due_date else datetime.max.date()))

    return render(request, 'tasks/all_tasks.html', {'tasks': tasks})

# Vista para listar las tareas vencidas
@login_required
def expired_tasks(request):
    expired_tasks = Task.objects.filter(user=request.user, due_date__lt=datetime.now(), completed=False)

    if not expired_tasks:
        messages.warning(request, 'No hay tareas vencidas por el momento. Buen Trabajo!')

    return render(request, 'tasks/expired_tasks.html', {"expired_tasks": expired_tasks})

# Vista para listar las tareas completadas
@login_required
def completed_tasks(request):
    completed_tasks = Task.objects.filter(user=request.user, completed=True)

    if not completed_tasks:
        messages.warning(request, 'No hay tareas completadas por el momento. A trabajar!')

    return render(request, 'tasks/completed_tasks.html', {"completed_tasks": completed_tasks})

# Vista para listar las tareas pendientes
@login_required
def pending_tasks(request):
    pending_tasks = Task.objects.filter(
        completed=False
    ).filter(
        Q(due_date__gte=timezone.now()) | Q(due_date__isnull=True)
    )

    if not pending_tasks:
        messages.warning(request, 'No hay tareas en progreso por el momento...')

    return render(request, 'tasks/pending_tasks.html', {"pending_tasks": pending_tasks})

# Crear una tarea
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Tarea añadida exitosamente.')
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

# Actualizar una tarea
@login_required
def task_update(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

# Marcar una tarea como completa o incompleta
@login_required
def update_status(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)    
    if request.method == 'POST':
        completed = f"task_{task.id}" in request.POST
        task.completed = completed
        task.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# Eliminar una tarea
@login_required
def task_delete(request, pk):
    if request.method == 'POST':
        task = Task.objects.get(pk=pk, user=request.user)
        task.delete()
        return redirect(request.META.get('HTTP_REFERER', 'home'))

