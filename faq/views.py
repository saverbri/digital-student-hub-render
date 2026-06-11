from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import FaqArticle
from .forms import FaqArticleForm

def is_staff_or_manager(user):
    return user.is_authenticated and (user.role in ['staff', 'manager', 'admin'] or user.is_superuser)

# Список статей (публичных) + поиск
def faq_list(request):
    articles = FaqArticle.objects.filter(is_published=True)
    
    # Поиск
    query = request.GET.get('q')
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'faq/list.html', {
        'page_obj': page_obj,
        'query': query,
    })

# Детальная страница статьи
def faq_detail(request, pk):
    article = get_object_or_404(FaqArticle, pk=pk, is_published=True)
    article.increment_views()
    return render(request, 'faq/detail.html', {'article': article})

# Управление статьями (список всех статей для сотрудников/менеджеров)
@login_required
@user_passes_test(is_staff_or_manager)
def faq_manage(request):
    articles = FaqArticle.objects.all().order_by('-created_at')
    paginator = Paginator(articles, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'faq/manage.html', {'page_obj': page_obj})

# Создание статьи
@login_required
@user_passes_test(is_staff_or_manager)
def faq_create(request):
    if request.method == 'POST':
        form = FaqArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Статья успешно создана')
            return redirect('faq:manage')
    else:
        form = FaqArticleForm()
    return render(request, 'faq/form.html', {'form': form, 'title': 'Создать статью'})

# Редактирование статьи
@login_required
@user_passes_test(is_staff_or_manager)
def faq_edit(request, pk):
    article = get_object_or_404(FaqArticle, pk=pk)
    if request.method == 'POST':
        form = FaqArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья обновлена')
            return redirect('faq:manage')
    else:
        form = FaqArticleForm(instance=article)
    return render(request, 'faq/form.html', {'form': form, 'title': 'Редактировать статью'})

# Удаление статьи
@login_required
@user_passes_test(is_staff_or_manager)
def faq_delete(request, pk):
    article = get_object_or_404(FaqArticle, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья удалена')
        return redirect('faq:manage')
    return render(request, 'faq/confirm_delete.html', {'article': article})