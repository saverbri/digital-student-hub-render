from django.urls import path
from . import views

urlpatterns = [
    path('staff/', views.staff_requests, name='staff_requests'),
    path('change-status/<int:pk>/', views.change_request_status, name='change_request_status'),
    path('chat/<int:request_id>/', views.chat_detail, name='chat_detail'),
]