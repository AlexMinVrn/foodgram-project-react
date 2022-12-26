from django_filters import CharFilter, FilterSet, NumberFilter, BooleanFilter

from recipes.models import Recipes


class CustomRecipeFilter(FilterSet):

    tags = CharFilter(field_name='tags__slug', lookup_expr='icontains')
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='get_is_in_shopping_cart')

    class Meta:
        model = Recipes
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping__user=user)
        return queryset
