from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime
import csv
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import AuditLog, UserSettings
from .forms import ProfileForm, SettingsForm
from django.contrib.auth import get_user_model

from requests_app.models import Request
from students.models import Student
from django.db.models import Count, Q

User = get_user_model()


def home(request):
    """Главная страница с адаптивным контентом"""
    context = {}
    if request.user.is_authenticated:
        total_requests = Request.objects.count()
        processing_requests = Request.objects.filter(status='processing').count()
        completed_requests = Request.objects.filter(status='completed').count()
        students_count = Student.objects.count()

        if request.user.role == 'student':
            recent_requests = Request.objects.filter(student=request.user).order_by('-created_at')[:5]
        else:
            recent_requests = Request.objects.all().order_by('-created_at')[:5]

        context.update({
            'total_requests': total_requests,
            'processing_requests': processing_requests,
            'completed_requests': completed_requests,
            'students_count': students_count,
            'recent_requests': recent_requests,
        })
    return render(request, 'home.html', context)


@login_required
def audit_log_list(request):
    if request.user.role not in ['manager', 'admin'] and not request.user.is_superuser:
        return HttpResponseForbidden("Доступ запрещён")
    
    logs = AuditLog.objects.all().order_by('-timestamp')
    
    user_id = request.GET.get('user')
    if user_id:
        logs = logs.filter(user_id=user_id)
    
    action = request.GET.get('action')
    if action:
        logs = logs.filter(action__icontains=action)
    
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        try:
            logs = logs.filter(timestamp__date__gte=datetime.strptime(date_from, '%Y-%m-%d'))
        except ValueError:
            pass
    if date_to:
        try:
            logs = logs.filter(timestamp__date__lte=datetime.strptime(date_to, '%Y-%m-%d'))
        except ValueError:
            pass
    
    if 'export_csv' in request.GET:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="audit_logs.csv"'
        writer = csv.writer(response)
        writer.writerow(['Время', 'Пользователь', 'Действие', 'IP-адрес', 'Детали'])
        for log in logs:
            writer.writerow([
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                str(log.user) if log.user else 'Аноним',
                log.action,
                log.ip_address,
                log.details
            ])
        return response
    
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    logs_page = paginator.get_page(page_number)
    
    users = User.objects.all().order_by('username')
    
    # Сохраняем текущие GET-параметры для пагинации
    current_params = request.GET.copy()
    if 'page' in current_params:
        current_params.pop('page')
    
    context = {
        'logs': logs_page,
        'users': users,
        'selected_user': user_id,
        'selected_action': action,
        'date_from': date_from,
        'date_to': date_to,
        'current_params': current_params.urlencode(),
    }
    return render(request, 'core/audit_log_list.html', context)


@login_required
def user_settings(request):
    # Автоматическое создание настроек, если их нет
    if not hasattr(request.user, 'settings'):
        UserSettings.objects.create(user=request.user)
    
    profile_form = ProfileForm(instance=request.user)
    settings_form = SettingsForm(instance=request.user.settings)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = ProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Профиль обновлён')
                return redirect('core:user_settings')
        elif 'settings_submit' in request.POST:
            settings_form = SettingsForm(request.POST, request.FILES, instance=request.user.settings)
            if settings_form.is_valid():
                settings_form.save()
                messages.success(request, 'Настройки сохранены')
                return redirect('core:user_settings')
        elif 'password_submit' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль изменён')
                return redirect('core:user_settings')
            else:
                messages.error(request, 'Ошибка при смене пароля')
        elif 'color_scheme_submit' in request.POST:
            new_scheme = request.POST.get('color_scheme')
            if new_scheme in dict(UserSettings.COLOR_SCHEMES).keys():
                request.user.settings.color_scheme = new_scheme
                request.user.settings.save()
                messages.success(request, 'Цветовая схема изменена')
            else:
                messages.error(request, 'Некорректная цветовая схема')
            return redirect('core:user_settings')

    context = {
        'profile_form': profile_form,
        'settings_form': settings_form,
        'password_form': password_form,
        'color_schemes': UserSettings.COLOR_SCHEMES,
    }
    return render(request, 'core/settings.html', context)


@login_required
@require_POST
def change_color_scheme_ajax(request):
    try:
        data = json.loads(request.body)
        new_scheme = data.get('color_scheme')
        if new_scheme in dict(UserSettings.COLOR_SCHEMES).keys():
            request.user.settings.color_scheme = new_scheme
            request.user.settings.save()
            return JsonResponse({'status': 'ok', 'color_scheme': new_scheme})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid scheme'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)