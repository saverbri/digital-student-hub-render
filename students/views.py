from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from requests_app.forms import RequestForm
from requests_app.models import Request

@login_required
def student_dashboard(request):
    # Получаем все обращения текущего студента
    requests = Request.objects.filter(student=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.student = request.user
            new_request.save()
            messages.success(request, 'Обращение успешно отправлено!')
            return redirect('student_dashboard')
    else:
        form = RequestForm()
    
    context = {
        'requests': requests,
        'form': form,
    }
    return render(request, 'students/dashboard.html', context)