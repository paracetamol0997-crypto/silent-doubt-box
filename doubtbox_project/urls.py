"""
URL configuration for doubtbox_project project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

handler403 = 'core.views.permission_denied_view'
handler404 = 'core.views.page_not_found_view'
