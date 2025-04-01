"""
URL configuration for myday project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events import views as event_views
from django.views.generic import TemplateView
from django.views.defaults import page_not_found, server_error
from django.http import HttpResponse

# Custom error views for debugging
def custom_500(request):
    """Custom 500 error handler that prints exception info."""
    import sys
    from django.views import debug
    from django.http import HttpResponse
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponse(error_html)

# Test view to check if basic routing works
def test_view(request):
    return HttpResponse("""
    <html>
        <head><title>MyDay Test Page</title></head>
        <body>
            <h1>MyDay Test Page</h1>
            <p>If you can see this, the Django server is running correctly.</p>
            <p>Debug mode: {}</p>
            <p>Allowed hosts: {}</p>
            <p>Static root: {}</p>
            <p>Database: {}</p>
        </body>
    </html>
    """.format(
        settings.DEBUG,
        settings.ALLOWED_HOSTS,
        settings.STATIC_ROOT,
        settings.DATABASES['default']['ENGINE']
    ))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('test/', test_view, name='test_view'),
]

# Add custom error handlers
handler400 = 'events.views.custom_bad_request'
handler403 = 'events.views.custom_permission_denied'
handler404 = 'events.views.custom_page_not_found'
handler500 = 'events.views.custom_server_error'

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
