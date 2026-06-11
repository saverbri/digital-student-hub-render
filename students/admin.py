from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'student_id', 'group', 'phone')
    list_filter = ('group',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'student_id')
    raw_id_fields = ('user',)