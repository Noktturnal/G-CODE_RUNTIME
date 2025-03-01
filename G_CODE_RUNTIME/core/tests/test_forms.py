import pytest
from django.contrib.auth.models import User  # Importuj User model
from core.models import Project, Task  # Importuj potřebné modely
from core.forms import TaskForm  # Importuj formulář


@pytest.mark.django_db
def test_task_form_invalid():
    """Test invalid task form (missing project)"""
    form_data = {'name': 'Test Task'}
    form = TaskForm(data=form_data)
    assert not form.is_valid()

    
@pytest.mark.django_db
def test_task_form_valid():
    """Test valid task form"""
    user = User.objects.create_user(username='testuser', password='password123')  # Vytvoř uživatele
    project = Project.objects.create(name='Test Project', description='A project for testing', owner=user)  # Přiřaď uživatele k projektu
    
    form_data = {
        'name': 'Test Task',  
        'project': project.id,
        'title': 'Task Title',  
        'description': 'Task description',  
        'assigned_to': user.id,  
        'due_date': '2025-03-01'  
    }
    
    form = TaskForm(data=form_data)
    
    if not form.is_valid():
        print(form.errors)  
    
    assert form.is_valid()
