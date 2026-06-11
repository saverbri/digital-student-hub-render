from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    details = models.JSONField(blank=True, default=dict)

    def __str__(self):
        return f"{self.timestamp}: {self.user} - {self.action}"

class UserSettings(models.Model):
    COLOR_SCHEMES = [
        ('cyan', 'Циан (по умолчанию)'),
        ('blue', 'Синий'),
        ('green', 'Зелёный'),
        ('purple', 'Фиолетовый'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    email_notifications = models.BooleanField(default=True, verbose_name='Уведомления на email')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    color_scheme = models.CharField(max_length=10, choices=COLOR_SCHEMES, default='cyan', verbose_name='Цветовая схема')

    def __str__(self):
        return f"Настройки {self.user.username}"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)