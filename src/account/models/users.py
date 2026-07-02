from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from account.managers import CustomUserManager  # Правильный импорт


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name='Телефон')
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'  # Вход по email
    REQUIRED_FIELDS = ['phone']  # phone будет запрашиваться при createsuperuser

    objects = CustomUserManager()  # Используем правильный менеджер

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'