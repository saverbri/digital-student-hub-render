from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('staff', 'Сотрудник'),
        ('manager', 'Руководитель'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    # Делаем email уникальным и обязательным
    email = models.EmailField(unique=True, blank=False, null=False)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"