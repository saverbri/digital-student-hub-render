from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'notifications/list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    # Если AJAX запрос, вернуть JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect('notification_list')

@login_required
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect('notification_list')