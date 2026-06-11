from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from requests_app.models import Request
from .models import Document

@login_required
def generate_document(request, request_id):
    req = get_object_or_404(Request, id=request_id, status='completed')
    
    # Создаём PDF в памяти
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Простой текст (без русского шрифта, но можно позже добавить)
    p.drawString(100, height - 100, f"Official document for request #{req.id}")
    p.drawString(100, height - 130, f"Student: {req.student.get_full_name()}")
    p.drawString(100, height - 160, f"Request type: {req.get_request_type_display()}")
    p.drawString(100, height - 190, f"Description: {req.description}")
    p.drawString(100, height - 220, f"Date: {req.created_at.strftime('%d.%m.%Y')}")
    p.drawString(100, height - 250, "Status: Completed")
    p.drawString(100, height - 280, "Digitally signed by system")
    p.showPage()
    p.save()
    
    buffer.seek(0)
    # Сохраняем файл
    doc, created = Document.objects.get_or_create(request=req)
    filename = f"document_{req.id}_{req.created_at.strftime('%Y%m%d')}.pdf"
    doc.file.save(filename, buffer, save=True)
    doc.doc_type = req.get_request_type_display()
    doc.save()
    
    messages.success(request, f'Документ для обращения #{req.id} сформирован')
    return redirect('staff_requests')