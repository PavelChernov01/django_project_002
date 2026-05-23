from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .models import Task, Tag, Project, Comment, Attachment
from .api_serializers import (
    TaskSerializer, UserSerializer, TagSerializer,
    ProjectSerializer, CommentSerializer, AttachmentSerializer
)
from account.models import User


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


# ============================================
# ЗАДАЧА 5: TOKEN AUTHENTICATION
# ============================================

class ObtainAuthTokenView(APIView):
    """Получение токена по email и паролю"""
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Authentication"],
        summary="Получить токен",
        description="Авторизация по email и паролю, возвращает токен для доступа к API",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'example': 'admin@example.com'},
                    'password': {'type': 'string', 'example': 'admin123'},
                }
            }
        },
        responses={200: {'description': 'Токен получен'}, 400: {'description': 'Ошибка'}}
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


class ProtectedTaskListView(APIView):
    """Список задач - только для аутентифицированных пользователей"""
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Tasks"],
        summary="Список задач (только для авторизованных)",
        description="Возвращает список задач. Требуется токен авторизации.",
        responses={200: TaskSerializer(many=True), 401: {'description': 'Не авторизован'}}
    )
    def get(self, request):
        tasks = Task.objects.all()[:20]
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@extend_schema(
    tags=["Authentication"],
    summary="Информация о пользователе",
    description="Возвращает информацию о текущем авторизованном пользователе",
    responses={200: {'description': 'Данные пользователя'}, 401: {'description': 'Не авторизован'}}
)
def get_user_info(request):
    """Получение информации о текущем пользователе"""
    return Response({
        'id': request.user.id,
        'email': request.user.email,
        'phone': request.user.phone,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'is_staff': request.user.is_staff,
    })