from .models import Notification
from django.core.mail import send_mail
from django.conf import settings

def create_notification(user, message, request_obj=None, link=None):
    # Создаём уведомление в БД
    Notification.objects.create(
        user=user,
        request=request_obj,
        message=message,
        link=link
    )
    # Отправляем email, если пользователь подписан и email указан
    if (hasattr(user, 'settings') and user.settings.email_notifications and user.email):
        send_mail(
            subject='Новое уведомление Digital Student Hub',
            message=message + f"\n\nСсылка: {link}\n\nЭто автоматическое сообщение.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )