"""
URL Configuration - Simple LMS

Routes:
  /admin/    → Django Admin panel
  /silk/     → Django Silk profiling dashboard
  /api/      → Django Ninja REST API (semua endpoint)
  /api/docs  → Swagger UI (auto-generated)
"""

from django.contrib import admin
from django.urls import path, include
from courses.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('silk/', include('silk.urls', namespace='silk')),
    path('', include('courses.urls')),
    path('api/', api.urls),
]
