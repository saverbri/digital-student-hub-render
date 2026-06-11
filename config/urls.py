from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('students/', include('students.urls')),
    path('requests/', include('requests_app.urls')),
    path('documents/', include('documents.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('notifications/', include('notifications.urls')),
    path('core/', include('core.urls', namespace='core')),
    path('faq/', include('faq.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)