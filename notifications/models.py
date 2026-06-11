from django.db import models
from django.conf import settings
from requests_app.models import Request

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')  # добавить
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Уведомление для {self.user.username}: {self.message[:30]}"