from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FavoriteView, IngredientsViewSet, RecipesViewSet,
                       ShoppingCartView, SubscriptionsList, TagsViewSet,
                       ToSubscribeView, download_shopping_cart)

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagsViewSet, basename='tag')
router.register('ingredients', IngredientsViewSet, basename='ingredient')
router.register('recipes', RecipesViewSet, basename='recipe')

urlpatterns = [
    path('users/<int:id>/subscribe/', ToSubscribeView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', SubscriptionsList.as_view(),
         name='subscriptions'),
    path('recipes/<int:id>/favorite/', FavoriteView.as_view(),
         name='favorite'),
    path('recipes/download_shopping_cart/', download_shopping_cart,
         name='download_shopping_cart'),
    path('recipes/<int:id>/shopping_cart/', ShoppingCartView.as_view(),
         name='shopping_cart'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
