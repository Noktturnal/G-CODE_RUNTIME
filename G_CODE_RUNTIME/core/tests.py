import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Project, Task, UserProfile

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='password')
    UserProfile.objects.create(user=user)  # Create UserProfile for the test user
    return user

@pytest.fixture
def project(user):
    return Project.objects.create(name='Test Project', description='Test Description', owner=user)

@pytest.fixture
def task(project):
    return Task.objects.create(project=project, title='Test Task', description='Test Description', due_date='2025-12-31')

@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_project_list_view(client, user):
    client.login(username='testuser', password='password')
    response = client.get(reverse('project_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_task_list_view(client, user, project):
    client.login(username='testuser', password='password')
    response = client.get(reverse('task_list', args=[project.id]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_task_detail_view(client, user, task):
    client.login(username='testuser', password='password')
    response = client.get(reverse('task_detail', args=[task.id]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_profile_view(client, user):
    client.login(username='testuser', password='password')
    response = client.get(reverse('user_profile', args=[user.id]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_task_view(client, user, project):
    client.login(username='testuser', password='password')
    response = client.get(reverse('create_task', args=[project.id]))
    assert response.status_code == 200
    response = client.post(reverse('create_task', args=[project.id]), {
        'title': 'New Task',
        'description': 'New Task Description',
        'due_date': '2025-12-31'
    })
    assert response.status_code == 302
    assert Task.objects.filter(title='New Task').exists()
