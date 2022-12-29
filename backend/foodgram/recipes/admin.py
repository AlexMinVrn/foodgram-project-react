from django.contrib import admin

from .models import (Favorites, Ingredients, IngredientsRecipes, Recipes,
                     RecipesTags, ShoppingCart, Tags)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'tags')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(RecipesTags)
class RecipesTagsAdmin(admin.ModelAdmin):
    list_display = ('recipes', 'tags')
    list_filter = ('tags',)


@admin.register(IngredientsRecipes)
class IngredientsRecipesAdmin(admin.ModelAdmin):
    list_display = ('recipes', 'ingredients', 'amount')
    list_filter = ('recipes', 'ingredients')


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    list_filter = ('user', 'recipes')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    list_filter = ('user', 'recipes')
