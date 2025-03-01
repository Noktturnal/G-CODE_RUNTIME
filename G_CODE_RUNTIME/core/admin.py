from django.contrib import admin
from .models import UserProfile, Project, Task, Comment, Tag, AnalysisResult

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(AnalysisResult)
