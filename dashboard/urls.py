from django.urls import path
from . import views

urlpatterns = [
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('reports/', views.reports, name='reports'),
]