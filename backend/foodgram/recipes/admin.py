from django.contrib import admin

from .models import (Favorites, Ingredients, IngredientsRecipes, Recipes,
                     RecipesTags, ShoppingCart, Tags)


class IngredientsRecipesInline(admin.TabularInline):
    model = IngredientsRecipes


class RecipesTagsInline(admin.TabularInline):
    model = RecipesTags


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'view_favorite_count')
    search_fields = ('name__startswith',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'
    inlines = [IngredientsRecipesInline, RecipesTagsInline]

    def view_favorite_count(self, obj):
        return obj.favorites.count()
    view_favorite_count.short_description = 'Всего в избранном'


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name__startswith',)


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
