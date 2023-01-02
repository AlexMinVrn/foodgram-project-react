from django.conf import settings
from django.conf.urls.static import static
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
    path('users/subscriptions/', SubscriptionsList.as_view(),
         name='subscriptions'),
    path('users/<int:id>/subscribe/', ToSubscribeView.as_view(),
         name='subscribe'),
    path('recipes/download_shopping_cart/', download_shopping_cart,
         name='download_shopping_cart'),
    path('recipes/<int:id>/shopping_cart/', ShoppingCartView.as_view(),
         name='shopping_cart'),
    path('recipes/<int:id>/favorite/', FavoriteView.as_view(),
         name='favorite'),
    path('rdf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
