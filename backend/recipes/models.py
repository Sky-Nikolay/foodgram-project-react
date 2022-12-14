"""Модели приложения `recipe`.
Models:
    1.Recipe:
        Основная модель приложения, через которую описываются рецепты.
    2.Tag:
        Модель для группировки рецептов по тэгам.
        Связана с Recipe через Many-To-Many.
    3.Ingredient:
        Модель описания ингредиентов.
        Связана с Recipe через модель AmountIngredient (Many-To-Many).
    4.Follow:
        Модель подписки на автора.
    5.IngredientRecipe:
        Модель для Ingredient и Recipe
        кол-во ингридиентов - amount
    6.FavoriteRecipe:
        Модель для добавления рецепта в избранное пользователя
    7.ShoppingList:
        Модель описания корзины пользователя
"""
from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Ингридиенты для рецепта.
    Связано с моделью базовой моделью Recipe через М2М (ingredients).
    Attributes:
        name(str):
            Название ингридиента.
            Ограничен по длине.
        measurement_unit(str):
            Единицы измерения ингридентов (граммы, штуки, литры и т.п.).
            Установлены ограничения по длине.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Тэги для рецептов.
    Связано с моделью базовой моделью Recipe - М2М.
    Attributes:
        name(str):
            Название. Установлены ограничения по длине и уникальности.
        color(str):
            Цвет тэга в HEX-кодировке.
        slug(str):
            Строчный слаг
    """
    name = models.CharField(
        max_length=60,
        unique=True,
        verbose_name='Имя'
    )
    color = ColorField(
        unique=True,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для рецептов. базовая модель
    Attributes:
        name(str):
            Название. Ограничения по длине.
        author(int):
            Автор рецепта. Связан с моделю User через ForeignKey.
        tags(int):
            Связь M2M с моделью Tag.
        ingredients(int):
            Связь M2M с моделью Ingredient. Связь создаётся посредством модели
            AmountIngredient с указанием количества ингридиента.
        pub_date(datetime):
            Дата добавления рецепта. Прописывается автоматически.
        image(str):
            Изображение рецепта. Указывает путь к изображению.
        text(str):
            Описание рецепта. Установлены ограничения по длине.
        cooking_time(int):
            Время приготовления рецепта.
            Ограничения минимальному значению.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes',
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, 'Время приготовления блюда должно быть больше 0',
        )],
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class IngredientRecipe(models.Model):
    """Количество ингридиентов в блюде.
    Модель связывает Recipe и Ingredient с указанием количества ингридиента.
    Attributes:
        recipe(int):
            Связаный рецепт. Связь через ForeignKey.
        ingredients(int):
            Связаный ингридиент. Связь через ForeignKey.
        amount(int):
            Количиства ингридиента в рецепте. валидация по значению
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_amounts',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amounts',
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1, 'Количество должно быть больше 0',
        )],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient')]

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class Follow(models.Model):
    """Подписки на автора.
    Модель связывает User и author
    Attributes:
        author(int):
            Автор рецепта. Связан с моделю User через ForeignKey
        user(int):
            пользователь. Связан с моделю User через ForeignKey
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription')]

    def __str__(self):
        return f'Пользователь {self.user} -> автор {self.author}'


class FavoriteRecipe(models.Model):
    """Избранные рецепты.
    Модель связывает User и Recipe
    Attributes:
        recipe(int):
            Связаный рецепт. Связь через ForeignKey.
        user(int):
            Пользователь. Связан с моделю User через ForeignKey
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingList(models.Model):
    """Модель корзины пользователя.
    Модель связывает User и Recipe
    Attributes:
        recipe(int):
            Связаный рецепт. Связь через ForeignKey.
        user(int):
            Пользователь. Связан с моделю User через ForeignKey
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_list',
        null=True,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shop_list',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shoppingList'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'
