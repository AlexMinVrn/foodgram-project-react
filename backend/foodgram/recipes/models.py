from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tags(models.Model):
    """Модель для тегов."""
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True)
    color = models.CharField(max_length=7, unique=True,
                             verbose_name='Цвет')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredients(models.Model):
    """Модель для ингредиентов."""
    name = models.CharField(
        'название продукта',
        max_length=200,
        db_index=True
    )
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=200
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Модель для рецептов."""
    name = models.CharField(
        'название рецепта',
        max_length=200,
        help_text='Введите название рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/',
        help_text='Загрузите фото к рецепту'
    )
    text = models.TextField(
        max_length=2000,
        verbose_name='Рецепт',
        help_text='Напишите процесс приготовления'
    )
    tags = models.ManyToManyField(Tags, related_name='recipes',
                                  through='RecipesTags')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        help_text='Введите время приготовления (в минутах)',
        validators=[MinValueValidator(1)]
    )
    ingredients = models.ManyToManyField(
        Ingredients, related_name='recipes',
        through='IngredientsRecipes',
        through_fields=('recipes', 'ingredients'),
        verbose_name='Ингредиенты'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipesTags(models.Model):
    """Модель связи рецептов и тегов."""
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                                verbose_name='Рецепт')
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE,
                             verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег для рецепта'
        verbose_name_plural = 'Теги для рецептов'
        constraints = [
            models.UniqueConstraint(
                name='unique_tag',
                fields=['recipes', 'tags'],
            ),
        ]


class IngredientsRecipes(models.Model):
    """Модель связи рецептов и ингредиентов."""
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                                verbose_name='Рецепт')
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE,
                                    verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f'{self.ingredients} в {self.recipes}'

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                name='unique_ingredient',
                fields=['recipes', 'ingredients'],
            ),
        ]


class Favorites(models.Model):
    """Модель добавления рецептов в избранное"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    recipes = models.ForeignKey(
        Recipes, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                name='unique_favorites',
                fields=['user', 'recipes'],
            ),
        ]


class ShoppingCart(models.Model):
    """Модель добавления рецептов в список покупок"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='customer',
        verbose_name='Пользователь'
    )
    recipes = models.ForeignKey(
        Recipes, on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Рецепт для покупок'
        verbose_name_plural = 'Рецепты для покупок'
        constraints = [
            models.UniqueConstraint(
                name='unique_shopping',
                fields=['user', 'recipes'],
            ),
        ]
