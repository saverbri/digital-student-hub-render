from django.urls import path
from . import views

urlpatterns = [
    path('generate/<int:request_id>/', views.generate_document, name='generate_document'),
]