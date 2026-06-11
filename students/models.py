from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True, verbose_name="Номер студенческого")
    group = models.CharField(max_length=50, verbose_name="Группа")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    address = models.TextField(blank=True, verbose_name="Адрес")

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"