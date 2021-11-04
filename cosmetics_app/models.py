from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    INCI = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.INCI


class Cosmetic(models.Model):
    full_name = models.CharField(unique=True, max_length=50)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    ingredient = models.ManyToManyField(Ingredient)

    @property
    def get_unique_functions(self):
        unique_functions = set()
        for ingredient in self.ingredient.all():
            for function in ingredient.function_set.all():
                unique_functions.add(function.name)
        return list(unique_functions)

    @property
    def get_unique_features(self):
        unique_features = set()
        for ingredient in self.ingredient.all():
            for function in ingredient.function_set.all():
                for feature in function.feature_set.all():
                    unique_features.add(feature.name)
        return list(unique_features)

    def __str__(self):
        return self.full_name


class Function(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    ingredient = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=50)
    function = models.ManyToManyField(Function)

    def __str__(self):
        return self.name
