from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
import subprocess
import os
import matplotlib.pyplot as plt
import io
import base64

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
    # Your file processing logic here
    results = "Processed results"
    tool_times = {}
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

def generate_pie_chart(tool_times):
    if not tool_times:
        return None  # Return None if tool_times is empty

    labels = list(tool_times.keys())
    sizes = list(tool_times.values())
    colors = plt.cm.Paired(range(len(tool_times)))

    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)  # Set figure size and DPI
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + string.decode('utf-8')
    plt.close(fig)  # Close the figure to free memory
    return uri

def register_view(request):
    return render(request, 'users/signup.html')

def login_view(request):
    return render(request, 'users/login.html')