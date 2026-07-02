import functools
from functools import lru_cache
from django.core.cache import cache, caches
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.shortcuts import render
from django.http import HttpResponse
from task_manager.models import Task, Project


# ============================================
# ЗАДАЧА 1: @lru_cache для рекурсивной функции
# ============================================

@lru_cache(maxsize=128)
def recursive_sum(numbers_tuple):
    """
    Рекурсивно считает сумму положительных чисел списка.
    Использует @lru_cache для кэширования результатов.
    """
    if not numbers_tuple:
        return 0
    first, rest = numbers_tuple[0], numbers_tuple[1:]
    if first > 0:
        return first + recursive_sum(rest)
    return recursive_sum(rest)


def test_lru_cache(request):
    """Тестовая вьюха для проверки lru_cache"""
    test_lists = [
        (1, 2, 3, 4, 5),
        (-1, 2, -3, 4, -5),
        (10, 20, 30),
        (1, 2, 3, 4, 5),
    ]

    results = []
    for lst in test_lists:
        result = recursive_sum(lst)
        results.append({
            'list': lst,
            'result': result,
        })

    cache_info = recursive_sum.cache_info()

    context = {
        'results': results,
        'cache_info': cache_info,
    }
    return render(request, 'task_manager/lru_cache_test.html', context)


# ============================================
# ЗАДАЧА 2: Кэш базы данных для вьюшек (30 минут)
# ============================================

@cache_page(60 * 30)
def cached_tasks_list(request):
    """Список задач с кэшированием на 30 минут"""
    tasks = Task.objects.select_related('project').prefetch_related('users').all()
    return render(request, 'task_manager/cached_tasks.html', {'tasks': tasks})


@cache_page(60 * 30)
def cached_projects_list(request):
    """Список проектов с кэшированием на 30 минут"""
    projects = Project.objects.all()
    return render(request, 'task_manager/cached_projects.html', {'projects': projects})


def invalidate_task_cache(request):
    """Инвалидация кэша при обновлении информации"""
    # Очищаем весь кэш (простой способ)
    cache.clear()
    return HttpResponse("Кэш очищен!")


# ============================================
# ЗАДАЧА 3: Кэш файловой системы (20 минут)
# ============================================

def get_cached_statistics():
    """Получение статистики с кэшированием на 20 минут"""
    file_cache = caches['file']
    stats = file_cache.get('site_statistics')
    if stats is None:
        stats = {
            'total_tasks': Task.objects.count(),
            'total_projects': Project.objects.count(),
            'completed_tasks': Task.objects.filter(status='completed').count(),
        }
        file_cache.set('site_statistics', stats, 1200)
    return stats


def cached_statistics_block(request):
    """HTML блок с кэшированной статистикой"""
    stats = get_cached_statistics()
    return render(request, 'task_manager/statistics_block.html', {'stats': stats})


def invalidate_file_cache(request):
    """Инвалидация файлового кэша"""
    file_cache = caches['file']
    file_cache.delete('site_statistics')
    return HttpResponse("Файловый кэш очищен!")