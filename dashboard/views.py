from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Count
from datetime import datetime, timedelta
from django.utils.timezone import now

# Импорты для экспорта отчётов
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

from requests_app.models import Request
from students.models import Student


@login_required
def manager_dashboard(request):
    if request.user.role not in ['manager', 'admin'] and not request.user.is_superuser:
        return HttpResponseForbidden("Доступ запрещён")
    
    # Данные для графиков
    status_stats = Request.objects.values('status').annotate(count=Count('id'))
    type_stats = Request.objects.values('request_type').annotate(count=Count('id'))
    
    # Динамика за последние 7 дней
    end_date = now().date()
    start_date = end_date - timedelta(days=6)
    date_labels = []
    date_counts = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        date_labels.append(day.strftime('%d.%m'))
        count = Request.objects.filter(created_at__date=day).count()
        date_counts.append(count)
    
    context = {
        'status_stats': list(status_stats),
        'type_stats': list(type_stats),
        'date_labels': date_labels,
        'date_counts': date_counts,
    }
    return render(request, 'dashboard/manager_dashboard.html', context)


@login_required
def reports(request):
    if request.user.role not in ['manager', 'admin'] and not request.user.is_superuser:
        return HttpResponseForbidden("Доступ запрещён")
    
    # Экспорт в Excel
    if 'export_excel' in request.GET:
        wb = Workbook()
        ws = wb.active
        ws.title = "Обращения"
        ws.append(['ID', 'Студент', 'Группа', 'Тип', 'Статус', 'Дата создания', 'Описание'])
        requests = Request.objects.all().order_by('-created_at')
        for req in requests:
            student_group = ''
            if hasattr(req.student, 'student'):
                student_group = req.student.student.group
            ws.append([
                req.id,
                req.student.get_full_name(),
                student_group,
                req.get_request_type_display(),
                req.get_status_display(),
                req.created_at.strftime('%d.%m.%Y %H:%M'),
                req.description[:100]
            ])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=requests_report.xlsx'
        wb.save(response)
        return response
    
    # Экспорт в PDF
    elif 'export_pdf' in request.GET:
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        p.drawString(100, height - 50, "Отчёт по обращениям студентов")
        p.drawString(100, height - 70, f"Дата: {datetime.now().strftime('%d.%m.%Y')}")
        y = height - 100
        requests = Request.objects.all().order_by('-created_at')[:30]
        for req in requests:
            if y < 50:
                p.showPage()
                y = height - 50
            p.drawString(50, y, f"{req.id}. {req.student.get_full_name()} - {req.get_request_type_display()} ({req.get_status_display()})")
            y -= 20
        p.showPage()
        p.save()
        buffer.seek(0)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=requests_report.pdf'
        response.write(buffer.getvalue())
        return response
    
    # Статистика для отображения на странице
    total_requests = Request.objects.count()
    status_stats = Request.objects.values('status').annotate(count=Count('id'))
    type_stats = Request.objects.values('request_type').annotate(count=Count('id'))
    students_count = Student.objects.count()
    
    context = {
        'total_requests': total_requests,
        'status_stats': status_stats,
        'type_stats': type_stats,
        'students_count': students_count,
    }
    return render(request, 'dashboard/reports.html', context)