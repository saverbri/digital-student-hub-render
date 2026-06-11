from django.contrib import admin
from .models import Request

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'request_type', 'status', 'created_at')
    list_filter = ('status', 'request_type')
    search_fields = ('student__username', 'description')