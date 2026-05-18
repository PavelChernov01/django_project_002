from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .models import Task, Tag, Project, Comment, Attachment
from .api_serializers import (
    TaskSerializer, UserSerializer, TagSerializer,
    ProjectSerializer, CommentSerializer, AttachmentSerializer
)


# ============================================
# ЗАДАЧА 4-5: APIView для задач (GET/POST/PUT/DELETE)
# ============================================

@extend_schema(tags=["Tasks"])
class TaskListAPIView(APIView):
    """GET: Список всех задач"""

    @extend_schema(
        summary="Получить список задач",
        description="Возвращает список всех задач с пагинацией",
        responses={200: TaskSerializer(many=True)}
    )
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Tasks"])
class TaskDetailAPIView(APIView):
    """GET: Получить задачу по ID"""

    @extend_schema(
        summary="Получить задачу",
        description="Возвращает задачу по указанному ID",
        responses={200: TaskSerializer, 404: {"description": "Задача не найдена"}}
    )
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response({"error": "Задача не найдена"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Tasks"])
class TaskCreateAPIView(APIView):
    """POST: Создать новую задачу"""

    @extend_schema(
        summary="Создать задачу",
        description="Создаёт новую задачу",
        request=TaskSerializer,
        responses={201: TaskSerializer, 400: {"description": "Ошибка валидации"}}
    )
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Tasks"])
class TaskUpdateAPIView(APIView):
    """PUT: Обновить задачу"""

    @extend_schema(
        summary="Обновить задачу",
        description="Обновляет существующую задачу",
        request=TaskSerializer,
        responses={200: TaskSerializer, 404: {"description": "Задача не найдена"}}
    )
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                updated_task = serializer.save()
                return Response(TaskSerializer(updated_task).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({"error": "Задача не найдена"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Tasks"])
class TaskDeleteAPIView(APIView):
    """DELETE: Удалить задачу"""

    @extend_schema(
        summary="Удалить задачу",
        description="Удаляет задачу по указанному ID",
        responses={204: {"description": "Успешно удалено"}, 404: {"description": "Задача не найдена"}}
    )
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"error": "Задача не найдена"}, status=status.HTTP_404_NOT_FOUND)


# ============================================
# ЗАДАЧА 7: Представление для тегов
# ============================================

@extend_schema(tags=["Tags"])
class TagListAPIView(APIView):
    """GET: Список всех тегов"""

    @extend_schema(
        summary="Получить список тегов",
        description="Возвращает список всех тегов",
        responses={200: TagSerializer(many=True)}
    )
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Tags"])
class TagDetailAPIView(APIView):
    """GET: Получить тег по ID"""

    def get(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except Tag.DoesNotExist:
            return Response({"error": "Тег не найден"}, status=status.HTTP_404_NOT_FOUND)


# ============================================
# ЗАДАЧА 8: Классовые представления для остальных моделей
# ============================================

@extend_schema(tags=["Projects"])
class ProjectListCreateAPIView(ListCreateAPIView):
    """GET: список проектов, POST: создание проекта"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


@extend_schema(tags=["Projects"])
class ProjectRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE для проекта"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


@extend_schema(tags=["Comments"])
class CommentListCreateAPIView(ListCreateAPIView):
    """GET: список комментариев, POST: создание комментария"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@extend_schema(tags=["Comments"])
class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE для комментария"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@extend_schema(tags=["Attachments"])
class AttachmentListCreateAPIView(ListCreateAPIView):
    """GET: список вложений, POST: создание вложения"""
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


@extend_schema(tags=["Attachments"])
class AttachmentRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """GET/DELETE для вложения (без UPDATE)"""
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer