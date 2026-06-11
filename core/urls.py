from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('settings/', views.user_settings, name='user_settings'),
    path('audit-logs/', views.audit_log_list, name='audit_log_list'),
    path('ajax/change-color-scheme/', views.change_color_scheme_ajax, name='change_color_scheme_ajax'),
]