# filepath: G_CODE_RUNTIME/G_CODE_RUNTIME/views.py
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')