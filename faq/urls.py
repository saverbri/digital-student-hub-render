from django.urls import path
from . import views

app_name = 'faq'

urlpatterns = [
    path('', views.faq_list, name='list'),
    path('<int:pk>/', views.faq_detail, name='detail'),
    path('manage/', views.faq_manage, name='manage'),
    path('create/', views.faq_create, name='create'),
    path('<int:pk>/edit/', views.faq_edit, name='edit'),
    path('<int:pk>/delete/', views.faq_delete, name='delete'),
]