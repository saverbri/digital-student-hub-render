from django.db import models
from django.conf import settings

class Request(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новое'),
        ('processing', 'В обработке'),
        ('completed', 'Завершено'),
        ('rejected', 'Отклонено'),
    )
    TYPE_CHOICES = (
        ('certificate', 'Справка об обучении'),
        ('transcript', 'Академическая справка'),
        ('other', 'Другое'),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests')
    request_type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name="Тип обращения")
    description = models.TextField(verbose_name="Описание", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_requests')

    def __str__(self):
        return f"{self.student.username} - {self.get_request_type_display()} ({self.status})"

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"


class Message(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages')
    text = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.author} on {self.request.id}"

    class Meta:
        ordering = ['created_at']