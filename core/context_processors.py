from requests_app.models import Request
from students.models import Student
from django.db.models import Q

def home_stats(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            total_requests = Request.objects.filter(student=request.user).count()
            processing_requests = Request.objects.filter(student=request.user, status='processing').count()
            completed_requests = Request.objects.filter(student=request.user, status='completed').count()
            recent_requests = Request.objects.filter(student=request.user).order_by('-created_at')[:5]
        else:
            total_requests = Request.objects.count()
            processing_requests = Request.objects.filter(status='processing').count()
            completed_requests = Request.objects.filter(status='completed').count()
            recent_requests = Request.objects.all().order_by('-created_at')[:5]
        students_count = Student.objects.count()
        return {
            'total_requests': total_requests,
            'processing_requests': processing_requests,
            'completed_requests': completed_requests,
            'students_count': students_count,
            'recent_requests': recent_requests,
        }
    return {}