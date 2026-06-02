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
from django.conf import settings
from django.conf.urls.static import static

from .api import api   # Django Ninja instance

urlpatterns = [
    path('admin/', admin.site.urls),
    path('silk/',  include('silk.urls', namespace='silk')),
    path('api/',   api.urls),   # Semua endpoint REST API + Swagger
]

# Serve media files di development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
