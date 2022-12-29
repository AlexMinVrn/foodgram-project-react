from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorites, Ingredients, IngredientsRecipes,
                            Recipes, ShoppingCart, Tags, User)
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Subscription

from .filters import CustomRecipeFilter
from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (FavoritesSerializer, IngredientsSerializer,
                          RecipesGetSerializer, RecipesWriteSerializer,
                          ShoppingCartSerializer, TagsSerializer,
                          ToSubscribeSerializer, UserExtendedSerializer)


class SubscriptionsList(generics.ListAPIView):
    serializer_class = UserExtendedSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user).annotate(
            recipes_count=Count('recipes'))


class ToSubscribeView(APIView):

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'following': id
        }
        serializer = ToSubscribeSerializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        following = get_object_or_404(User, id=id)
        if Subscription.objects.filter(
           user=request.user, following=following).exists():
            subscription = get_object_or_404(
                Subscription, user=request.user, following=following
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для доступа к тегам."""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для доступа к тегам."""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipesViewSet(viewsets.ModelViewSet):
    """ViewSet для доступа к рецептам."""
    queryset = Recipes.objects.all()
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomRecipeFilter
    pagination_class = LimitOffsetPagination
    ordering = ['-pub_date']

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return RecipesGetSerializer
        return RecipesWriteSerializer


class FavoriteView(APIView):

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipes': id
        }
        serializer = FavoritesSerializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipes = get_object_or_404(Recipes, id=id)
        if Favorites.objects.filter(
           user=request.user, recipes=recipes).exists():
            favorites = get_object_or_404(
                Favorites, user=request.user, recipes=recipes
            )
            favorites.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartView(APIView):

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipes': id
        }
        serializer = ShoppingCartSerializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipes = get_object_or_404(Recipes, id=id)
        if ShoppingCart.objects.filter(
           user=request.user, recipes=recipes).exists():
            shoppingcart = get_object_or_404(
                ShoppingCart, user=request.user, recipes=recipes
            )
            shoppingcart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def download_shopping_cart(request):
    shopping_list = "Список покупок:"
    ingredients = IngredientsRecipes.objects.filter(
        recipes__shopping__user=request.user
    ).values(
        'ingredients__name', 'ingredients__measurement_unit'
    ).annotate(amount=Sum('amount'))
    for num, i in enumerate(ingredients):
        shopping_list += (
            f"\n{i['ingredients__name']} - "
            f"{i['amount']} {i['ingredients__measurement_unit']}"
        )
        if num < ingredients.count() - 1:
            shopping_list += ', '
    filename = "shopping_list.txt"
    response = HttpResponse(shopping_list, 'Content-Type: application/txt')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response