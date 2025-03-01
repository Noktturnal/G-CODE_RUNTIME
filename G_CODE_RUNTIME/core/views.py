from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, TaskForm
from .models import Project, Task, UserProfile
import subprocess
import os

def home_view(request):
    """View for the home page."""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file
            file = request.FILES['file']
            results, tool_times = process_file(file)
            return render(request, 'home.html', {'form': form, 'results': results, 'tool_times': tool_times})
    else:
        form = UploadFileForm()
    return render(request, 'home.html', {'form': form})

def process_file(file):
    """Process the uploaded file and extract results and tool times."""
    # Save the uploaded file to a temporary location
    temp_file_path = '/tmp/uploaded_file'
    with open(temp_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    
    # Run the algorithm and capture the output
    result = subprocess.run(['python3', '/home/noktturnal/PycharmProjects/G-CODE_RUNTIME/G_CODE_RUNTIME/runtime_algorithm/utils.py', temp_file_path], capture_output=True, text=True)
    output = result.stdout

    # Extract results and tool times from the output
    results, tool_times = extract_results_and_tool_times(output)
    return results, tool_times

def extract_results_and_tool_times(output):
    """Extract results and tool times from the algorithm output."""
    results = []
    tool_times = {}
    lines = output.split('\n')
    start_collecting = False
    for line in lines:
        if "===== RESULTS =====" in line:
            start_collecting = True
        if start_collecting:
            results.append(line)
            if line.startswith("Tool"):
                parts = line.split()
                if len(parts) >= 8:
                    tool = parts[1].strip(':')
                    total_time = float(parts[7])
                    tool_times[tool] = total_time
    return '\n'.join(results), tool_times

def register_view(request):
    """View for user registration."""
    return render(request, 'users/signup.html')

def login_view(request):
    """View for user login."""
    return render(request, 'users/login.html')

def about_view(request):
    """View for the about page."""
    return render(request, 'about.html')

@login_required
def project_list_view(request):
    """View for listing projects."""
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def task_list_view(request, project_id):
    """View for listing tasks in a project."""
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)
    return render(request, 'task_list.html', {'project': project, 'tasks': tasks})

@login_required
def task_detail_view(request, task_id):
    """View for task details."""
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})

@login_required
def user_profile_view(request, user_id):
    """View for user profile."""
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    return render(request, 'user_profile.html', {'user_profile': user_profile})

@login_required
def create_task_view(request, project_id):
    """View for creating a new task."""
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('task_list', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form, 'project': project})