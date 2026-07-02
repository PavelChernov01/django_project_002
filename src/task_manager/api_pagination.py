from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# ============================================
# ЗАДАЧА 1: Стандартная пагинация (10 элементов)
# ============================================
class UserPagination(PageNumberPagination):
    """Пагинация для пользователей"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })


# ============================================
# ЗАДАЧА 2: Кастомный класс пагинации (5 элементов, можно менять до 50)
# ============================================
class CustomTaskPagination(PageNumberPagination):
    """Кастомная пагинация для задач"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'total_items': self.page.paginator.count,
            'results': data
        })