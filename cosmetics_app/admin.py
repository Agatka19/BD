from django.contrib import admin

from .models import Brand, Type, Ingredient, Cosmetic, Function, Feature

admin.site.register(Brand)
admin.site.register(Type)
admin.site.register(Cosmetic)
admin.site.register(Function)
admin.site.register(Feature)
admin.site.register(Ingredient)
