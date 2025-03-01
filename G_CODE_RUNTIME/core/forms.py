from django import forms
from .models import Task, UserProfile

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file', required=False)
    save_results = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']