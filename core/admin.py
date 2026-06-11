from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'timestamp', 'ip_address')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'action', 'ip_address')
    readonly_fields = ('timestamp', 'ip_address', 'details')
    date_hierarchy = 'timestamp'