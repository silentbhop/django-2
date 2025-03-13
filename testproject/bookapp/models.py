from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Book(models.Model):
    title = models.CharField('Название', max_length=50)
    author = models.CharField('Автор', max_length=50)
    price = models.FloatField('Цена')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return '/'
    
class UserRole(models.TextChoices):
    USER = "user", "Обычный пользователь"
    ADMIN = "admin", "Администратор"

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    def __str__(self):
        return self.username

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Имя пользователя обязятельно')
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRole.ADMIN)

        if password is None:
            raise ValueError("Суперпользователь должен иметь пароль")
        
        return self.create_user(username, email, password, **extra_fields)