from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models

from .managers import UserManager


class UserRoles(models.TextChoices):
    ADMIN = 'admin', 'Администратор'
    USER = 'user', 'Пользователь'


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона', null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=UserRoles.choices, default=UserRoles.USER)
    image = models.ImageField(upload_to='users_img', verbose_name='Аватар', null=True, blank=True)

    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'role', 'image']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
