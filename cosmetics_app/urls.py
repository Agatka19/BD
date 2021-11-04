from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('suggestions', views.suggestions, name='suggestions'),
    path('ingredients', views.ingredients, name='ingredients'),
    path('cosmetics', views.cosmetics, name='cosmetics'),
    path('functions', views.functions, name='functions'),
    path('features', views.features, name='features'),
    path('types', views.types, name='types'),
    path('brands', views.brands, name='brands'),
    path('create', views.create, name='create')
]
