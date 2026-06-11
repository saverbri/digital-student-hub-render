# requests_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Request
from notifications.utils import create_notification
from django.http import JsonResponse
from .models import Message


@login_required
def staff_requests(request):
    if request.user.role not in ['staff', 'manager', 'admin'] and not request.user.is_superuser:
        messages.error(request, 'Доступ запрещён')
        return redirect('home')
    
    requests_list = Request.objects.all().order_by('-created_at')
    return render(request, 'requests_app/staff_requests.html', {'requests_list': requests_list})

@login_required
def change_request_status(request, pk):
    if request.user.role not in ['staff', 'manager', 'admin'] and not request.user.is_superuser:
        messages.error(request, 'Доступ запрещён')
        return redirect('home')
    
    req = get_object_or_404(Request, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Request.STATUS_CHOICES).keys():
            req.status = new_status
            req.processed_by = request.user
            req.save()
            
            # Создаём уведомление для студента
            status_display = dict(Request.STATUS_CHOICES).get(new_status)
            create_notification(
                user=req.student,
                message=f"Статус вашего обращения №{req.id} изменён на '{status_display}'",
                request_obj=req,
                link="/students/dashboard/"
            )
            
            messages.success(request, f'Статус обращения #{req.id} изменён на "{req.get_status_display()}"')
        else:
            messages.error(request, 'Некорректный статус')
        return redirect('staff_requests')
    return redirect('staff_requests')

@login_required
def chat_detail(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    # Проверка доступа: студент — только свои заявки, сотрудник/менеджер/админ — любые
    if request.user.role == 'student' and req.student != request.user:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Доступ запрещён")
    
    messages = req.messages.all()
    
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            msg = Message.objects.create(
                request=req,
                author=request.user,
                text=text
            )
            # Уведомление другому участнику
            if request.user == req.student:
                recipient = req.processed_by if req.processed_by else None
            else:
                recipient = req.student
            if recipient:
                create_notification(
                    user=recipient,
                    message=f"Новое сообщение в обращении #{req.id}",
                    request_obj=req,
                    link=f"/requests/chat/{req.id}/"
                )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'ok', 'text': text, 'author': request.user.username})
            else:
                return redirect('chat_detail', request_id=req.id)
    
    context = {
        'request_obj': req,
        'messages': messages,
    }
    return render(request, 'requests_app/chat_detail.html', context)