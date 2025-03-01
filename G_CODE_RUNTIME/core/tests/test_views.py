import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from core.models import Project, Task, AnalysisResult
from core.forms import UploadFileForm, TaskForm
from core.models import Project, Task, AnalysisResult, UserProfile


@pytest.mark.django_db
def test_home_view_authenticated():
    """Test home view for authenticated users."""
    user = User.objects.create_user(username='testuser', password='password123')
    client = Client()
    client.login(username='testuser', password='password123')

    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_home_view_post_request():
    """Test home view for POST requests."""
    user = User.objects.create_user(username='testuser', password='password123')
    client = Client()
    client.login(username='testuser', password='password123')

    file_data = {'file': 'testfile.gcode'}
    response = client.post(reverse('home'), {'file': file_data, 'save_results': True})

    # Assuming that the algorithm runs and outputs results
    assert response.status_code == 200
    assert 'results' in response.context
    assert 'tool_times' in response.context

@pytest.mark.django_db
def test_project_list_view():
    """Test project list view for authenticated users."""
    user = User.objects.create_user(username='testuser', password='password123')
    client = Client()
    client.login(username='testuser', password='password123')

    project = Project.objects.create(name="Test Project", description="Test Project Description", owner=user)

    response = client.get(reverse('project_list'))
    assert response.status_code == 200
    assert 'projects' in response.context
    assert project.name in str(response.content)

@pytest.mark.django_db
def test_task_list_view():
    """Test task list view for a specific project."""
    user = User.objects.create_user(username='testuser', password='password123')
    client = Client()
    client.login(username='testuser', password='password123')

    project = Project.objects.create(name="Test Project", description="Test Project Description", owner=user)
    task = Task.objects.create(project=project, title="Test Task", description="Test Task Description", assigned_to=user, due_date="2025-04-01", completed=False)

    response = client.get(reverse('task_list', args=[project.id]))
    assert response.status_code == 200
    assert task.title in str(response.content)

@pytest.mark.django_db
def test_task_detail_view():
    """Test task detail view."""
    user = User.objects.create_user(username='testuser', password='password123')
    client = Client()
    client.login(username='testuser', password='password123')

    project = Project.objects.create(name="Test Project", description="Test Project Description", owner=user)
    task = Task.objects.create(project=project, title="Test Task", description="Test Task Description", assigned_to=user, due_date="2025-04-01", completed=False)

    response = client.get(reverse('task_detail', args=[task.id]))
    assert response.status_code == 200
    assert task.title in str(response.content)

@pytest.mark.django_db
def test_user_profile_view():
    """Test user profile view."""
    user = User.objects.create_user(username='testuser', password='password123')
    client = Client()
    client.login(username='testuser', password='password123')

    user_profile, created = UserProfile.objects.get_or_create(user=user,defaults={"bio": "This is a bio."})
    analysis_result = AnalysisResult.objects.create(user=user, file_name="test_file.gcode", results="Test Results", tool_times={"tool_1": 120})

    response = client.get(reverse('user_profile', args=[user.id]))
    assert response.status_code == 200
    assert 'user_profile' in response.context
    assert 'analysis_results' in response.context

@pytest.mark.django_db
def test_create_task_view():
    """Test task creation view."""
    user = User.objects.create_user(username='testuser', password='password123')
    client = Client()
    client.login(username='testuser', password='password123')

    project = Project.objects.create(name="Test Project", description="Test Project Description", owner=user)
    form_data = {'title': 'New Task', 'description': 'Description of new task', 'assigned_to': user.id, 'due_date': '2025-04-01'}

    response = client.post(reverse('create_task', args=[project.id]), data=form_data)
    assert response.status_code == 302  # Redirect after successful creation
    assert Task.objects.count() == 1
    assert Task.objects.first().title == 'New Task'

@pytest.mark.django_db
def test_delete_analysis_result_view():
    """Test analysis result deletion view."""
    user = User.objects.create_user(username='testuser', password='password123')
    client = Client()
    client.login(username='testuser', password='password123')

    analysis_result = AnalysisResult.objects.create(user=user, file_name="test_file.gcode", results="Test Results", tool_times={"tool_1": 120})

    response = client.post(reverse('delete_analysis_result', args=[analysis_result.id]))
    assert response.status_code == 302  # Redirect after deletion
    assert AnalysisResult.objects.count() == 0
