from django.db import models
from requests_app.models import Request

class Document(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, related_name='document')
    file = models.FileField(upload_to='documents/')
    generated_at = models.DateTimeField(auto_now_add=True)
    doc_type = models.CharField(max_length=100)

    def __str__(self):
        return f"Документ к обращению {self.request.id}"