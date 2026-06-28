from rest_framework import serializers
from .models import Task, Tag, Project, Comment, Attachment
from account.models import User


# ============================================
# ЗАДАЧА 4: Сериализаторы, не привязанные к модели (для задач и пользователей)
# ============================================

class UserSerializer(serializers.Serializer):
    """Сериализатор для пользователя (не привязан к модели)"""
    id = serializers.IntegerField(read_only=True)
    phone = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class TaskSerializer(serializers.Serializer):
    """Сериализатор для задачи (не привязан к модели)"""
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES)
    priority = serializers.IntegerField(min_value=1, max_value=4)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    project_id = serializers.IntegerField()
    user_ids = serializers.ListField(child=serializers.IntegerField(), required=False)

    def create(self, validated_data):
        user_ids = validated_data.pop('user_ids', [])
        project_id = validated_data.pop('project_id')
        project = Project.objects.get(id=project_id)
        task = Task.objects.create(project=project, **validated_data)
        if user_ids:
            task.users.set(user_ids)
        return task

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)

        if 'project_id' in validated_data:
            instance.project = Project.objects.get(id=validated_data['project_id'])

        instance.save()

        if 'user_ids' in validated_data:
            instance.users.set(validated_data['user_ids'])

        return instance


# ============================================
# ЗАДАЧА 6: Сериализаторы для остальных моделей
# ============================================

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.first_name', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'owner_name', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.first_name', read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'task', 'task_title', 'author', 'author_name', 'created_at']


class AttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ['id', 'filename', 'file', 'file_url', 'task', 'uploaded_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None


# ============================================
# НОВЫЕ СЕРИАЛИЗАТОРЫ ДЛЯ ФИЛЬТРАЦИИ И ПАГИНАЦИИ
# ============================================

class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка пользователей"""
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'first_name', 'last_name', 'is_active']


class TaskListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка задач"""
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'project', 'created_at']


# ============================================
# СЕРИАЛИЗАТОРЫ ДЛЯ CELERY BEAT (ЗАДАЧА 8)
# ============================================

from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule


class IntervalScheduleSerializer(serializers.ModelSerializer):
    """Сериализатор для интервальных расписаний"""
    class Meta:
        model = IntervalSchedule
        fields = ['id', 'every', 'period']
        read_only_fields = ['id']


class CrontabScheduleSerializer(serializers.ModelSerializer):
    """Сериализатор для crontab расписаний"""
    class Meta:
        model = CrontabSchedule
        fields = ['id', 'minute', 'hour', 'day_of_month', 'month_of_year', 'day_of_week']
        read_only_fields = ['id']


class SolarScheduleSerializer(serializers.ModelSerializer):
    """Сериализатор для solar расписаний (восход/закат)"""
    class Meta:
        model = SolarSchedule
        fields = ['id', 'event', 'latitude', 'longitude']
        read_only_fields = ['id']


class PeriodicTaskSerializer(serializers.ModelSerializer):
    """Сериализатор для периодических задач"""
    interval_detail = IntervalScheduleSerializer(source='interval', read_only=True)
    crontab_detail = CrontabScheduleSerializer(source='crontab', read_only=True)
    solar_detail = SolarScheduleSerializer(source='solar', read_only=True)

    class Meta:
        model = PeriodicTask
        fields = [
            'id', 'name', 'task', 'interval', 'interval_detail',
            'crontab', 'crontab_detail', 'solar', 'solar_detail',
            'enabled', 'one_off', 'start_time', 'args', 'kwargs',
            'expires', 'date_changed', 'description'
        ]
        read_only_fields = ['id', 'date_changed']

    def create(self, validated_data):
        validated_data.pop('interval_detail', None)
        validated_data.pop('crontab_detail', None)
        validated_data.pop('solar_detail', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('interval_detail', None)
        validated_data.pop('crontab_detail', None)
        validated_data.pop('solar_detail', None)
        return super().update(instance, validated_data)