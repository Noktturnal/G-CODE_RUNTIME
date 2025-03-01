from django.shortcuts import render
from .forms import UploadFileForm
import subprocess
import os

def home_view(request):
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
    return render(request, 'users/signup.html')

def login_view(request):
    return render(request, 'users/login.html')

def about_view(request):
    return render(request, 'about.html')