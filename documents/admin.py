from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'doc_type', 'generated_at')
    list_filter = ('doc_type', 'generated_at')
    search_fields = ('request__student__username', 'request__id')
    readonly_fields = ('generated_at',)