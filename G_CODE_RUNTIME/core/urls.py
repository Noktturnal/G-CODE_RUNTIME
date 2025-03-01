from django.urls import path
from .views import home_view, project_list_view, task_list_view, task_detail_view, user_profile_view, create_task_view

urlpatterns = [
    path('', home_view, name='home'),
    path('projects/', project_list_view, name='project_list'),
    path('projects/<int:project_id>/tasks/', task_list_view, name='task_list'),
    path('tasks/<int:task_id>/', task_detail_view, name='task_detail'),
    path('users/<int:user_id>/', user_profile_view, name='user_profile'),
    path('projects/<int:project_id>/tasks/create/', create_task_view, name='create_task'),
]