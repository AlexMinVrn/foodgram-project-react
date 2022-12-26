import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from foodgram import settings
from recipes.models import (Ingredients, Tags, Recipes, IngredientsRecipes,
                            RecipesTags, Favorites, ShoppingCart)
from users.models import Subscription, User


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей"""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        read_only_fields = ['id']


class CustomUserSerializer(UserSerializer):
    """Сериализатор для просмотра пользователей"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'id', 'email', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(
            user=request.user, following=obj
        ).exists()


class RecipesMiniSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов в других моделях"""
    class Meta:
        model = Recipes
        fields = ('name', 'image', 'cooking_time', 'id')


class UserExtendedSerializer(CustomUserSerializer):
    """Сериализатор для пользователей на кого подписался"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'id', 'email', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        recipes_limit = self.context.get(
            'recipes_limit',
            settings.DEFAULT_RECIPES_LIMIT
        )
        recipes = obj.recipes.all()[:recipes_limit]
        return RecipesMiniSerializer(
            recipes, many=True, context=self.context
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class ToSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки на пользователя"""
    class Meta:
        model = Subscription
        fields = ['user', 'following']

    def validate(self, data):
        user = self.context.get('request').user
        following_id = data['following'].id
        if Subscription.objects.filter(user=user,
                                       following__id=following_id).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя')
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписываться на себя!')
        return data

    def to_representation(self, instance):
        return UserExtendedSerializer(instance.following, context={
            'request': self.context.get('request')
        }).data


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    class Meta:
        model = Tags
        fields = '__all__'


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""
    class Meta:
        model = Ingredients
        fields = '__all__'


class FavoritesSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов"""

    class Meta:
        model = Favorites
        fields = ['user', 'recipes']

    def to_representation(self, instance):
        return RecipesMiniSerializer(instance.recipes, context={
            'request': self.context.get('request')
        }).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецептов в список покупок"""
    class Meta:
        model = ShoppingCart
        fields = ['user', 'recipes']

    def to_representation(self, instance):
        return RecipesMiniSerializer(instance.recipes, context={
            'request': self.context.get('request')
        }).data


class AddIngredientsRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для связи ингредиентов и рецептов при создании рецептов"""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsRecipes
        fields = ['id', 'amount']


class IngredientsRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для связи ингредиентов и рецептов"""
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit'
    )

    class Meta:
        model = IngredientsRecipes
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipesGetSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецептов."""
    tags = TagsSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    author = CustomUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        ordering = ['-pub_date']
        model = Recipes
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]

    def get_ingredients(self, obj):
        ingredients = IngredientsRecipes.objects.filter(recipes=obj)
        return IngredientsRecipesSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorites.objects.filter(
            user=request.user, recipes_id=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipes_id=obj
        ).exists()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipesWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания, изменения и удаления рецептов."""
    ingredients = AddIngredientsRecipesSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(), many=True,
    )
    # image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = [
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        ]
        read_only_fields = ['author']

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        list = []
        for ingredient in ingredients:
            amount = ingredient['amount']
            if int(amount) < 1:
                raise serializers.ValidationError({
                   'amount': 'Количество ингредиента не может быть равным 0'
                })
            if ingredient['id'] in list:
                raise serializers.ValidationError({
                   'ingredient': 'Ингредиенты не должны повторяться'
                })
            list.append(ingredient['id'])
        return data

    def create_ingredients(self, ingredients, recipe):
        for item in ingredients:
            ingredient = Ingredients.objects.get(id=item['id'])
            print(ingredient)
            IngredientsRecipes.objects.create(
                ingredients=ingredient, recipes=recipe, amount=item['amount']
            )

    def create_tags(self, tags, recipe):
        for tag in tags:
            RecipesTags.objects.create(recipes=recipe, tags=tag)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipes.objects.create(author=author, **validated_data)
        self.create_ingredients(ingredients, recipe)
        # recipe.tags.set(tags)
        self.create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        RecipesTags.objects.filter(recipes=instance).delete()
        IngredientsRecipes.objects.filter(recipes=instance).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.create_ingredients(ingredients, instance)
        self.create_tags(tags, instance)
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        if validated_data.get('image'):
            instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipesGetSerializer(instance, context={
            'request': self.context.get('request')
        }).data
