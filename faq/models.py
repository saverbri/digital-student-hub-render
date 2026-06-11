from django.db import models
from django.conf import settings
from django.utils import timezone

class FaqArticle(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'Общие вопросы'),
        ('documents', 'Документы и справки'),
        ('technical', 'Технические проблемы'),
        ('other', 'Другое'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general', verbose_name='Категория')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Статья FAQ'
        verbose_name_plural = 'Статьи FAQ'
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])