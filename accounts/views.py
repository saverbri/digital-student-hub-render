from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import StudentRegistrationForm

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать.')
            return redirect('student_dashboard')
        else:
            # Выводим ошибки формы для отладки
            messages.error(request, 'Ошибка регистрации. Проверьте правильность заполнения.')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})