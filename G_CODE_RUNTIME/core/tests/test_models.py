import pytest
from django.contrib.auth.models import User
from core.models import UserProfile, Project, Task, Comment, Tag, AnalysisResult

@pytest.mark.django_db
def test_create_user_profile():
    """Test creation of UserProfile model"""
    user = User.objects.create_user(username='testuser', password='password123')
    
    # Ensure no UserProfile exists for this user before creating
    UserProfile.objects.filter(user=user).delete()
    
    profile = UserProfile.objects.create(user=user, bio="This is a test bio.")
    
    assert profile.user == user
    assert profile.bio == "This is a test bio."

@pytest.mark.django_db
def test_create_project():
    """Test creation of Project model"""
    user = User.objects.create_user(username='testuser', password='password123')
    project = Project.objects.create(name="Test Project", description="Test Project Description", owner=user)
    
    assert project.name == "Test Project"
    assert project.owner == user
    assert project.description == "Test Project Description"

@pytest.mark.django_db
def test_add_collaborator():
    """Test adding collaborators to a Project"""
    user1 = User.objects.create_user(username='testuser1', password='password123')
    user2 = User.objects.create_user(username='testuser2', password='password123')
    project = Project.objects.create(name="Test Project", description="Test Project Description", owner=user1)
    
    project.collaborators.add(user2)
    
    assert user2 in project.collaborators.all()

@pytest.mark.django_db
def test_create_task():
    """Test creation of Task model"""
    user = User.objects.create_user(username='testuser', password='password123')
    project = Project.objects.create(name="Test Project", description="Test Project Description", owner=user)
    task = Task.objects.create(
        project=project, 
        title="Test Task", 
        description="Task description", 
        assigned_to=user, 
        due_date="2025-04-01", 
        completed=False
    )
    
    assert task.title == "Test Task"
    assert task.project == project
    assert task.assigned_to == user
    assert task.due_date == "2025-04-01"
    assert task.completed is False

@pytest.mark.django_db
def test_create_comment():
    """Test creation of Comment model"""
    user = User.objects.create_user(username='testuser', password='password123')
    project = Project.objects.create(name="Test Project", description="Test Project Description", owner=user)
    task = Task.objects.create(
        project=project, 
        title="Test Task", 
        description="Task description", 
        assigned_to=user, 
        due_date="2025-04-01", 
        completed=False
    )
    comment = Comment.objects.create(task=task, author=user, content="This is a test comment.")
    
  
