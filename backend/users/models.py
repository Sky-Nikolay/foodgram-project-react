"""Приложение Users для работы с моделью пользователей.
Модели и методы для настроийки и управления пользователями
приложения Foodgram. За основу взята модель AbstractUser из Django
переопределены следующие атрибуты:
    email(str):
        Адрес email пользователя.
        Проверка формата производится внутри Dlango.
        Установлено ограничение по максимальной длине.
    username(str):
        Юзернейм пользователя.
        Установлены ограничения по минимальной и максимальной длине.
        Для ввода разрешены только буквы.
    first_name(str):
        Реальное имя пользователя.
        Установлено ограничение по максимальной длине.
    last_name(str):
        Реальная фамилия пользователя.
        Установлено ограничение по максимальной длине.
    is_subscribed(int):
        Ссылки на id связанных пользователей.
"""
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=200,
        verbose_name='Email',
        unique=True,
    )
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимые символы'
        )]
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    is_subscribed = models.ManyToManyField(
        verbose_name='Подписка',
        related_name='subscribers',
        to='self',
        symmetrical=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username}: {self.email}'
