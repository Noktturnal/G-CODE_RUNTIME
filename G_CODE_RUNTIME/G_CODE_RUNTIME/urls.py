from django.contrib import admin
from django.urls import path, include
from core.views import home_view, about_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('users/', include('users.urls')),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Use Django's built-in LogoutView
    path('', include('core.urls')),
]