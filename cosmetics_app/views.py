from django.shortcuts import render

from .models import Cosmetic
from .models import Type
from .models import Brand
from .models import Ingredient
from .models import Feature
from .models import Function


def index(request):
    return render(request, 'cosmetics_app/index.html')


def suggestions(request):
    type_name = request.GET.get('type_name', '')
    brand_country = request.GET.get('brand_country', '')
    feature_name = request.GET.get('ingredient_function_feature', '')

    types_list = [t.strip() for t in type_name.split(sep=',')]
    country_list = [b.strip() for b in brand_country.split(sep=',')]

    requested_feature_set = {feature.strip() for feature in feature_name.split(sep=',')}

    # Wybiera wszystkie kosmetyki gdzie pojawi sie przynajmniej jeden z wpisanych 'type', 'country' i 'feature'
    products = Cosmetic.objects.filter(type__name__in=types_list, brand__country__in=country_list,
                                       ingredient__function__feature__name__in=requested_feature_set).distinct().order_by(
        'id')

    #  Wybiera tylko te kosmetyki gdzie pojawia sie wszystkie wpisane 'features'
    good_products = []

    for product in products:
        # wybieram cechy jakie odpowiadaja skladnikom tego produktu
        product_features = Feature.objects.filter(function__ingredient__cosmetic=product).distinct()
        product_features_set = {feature.name for feature in product_features}
        if requested_feature_set <= product_features_set:
            good_products.append(product)

    return render(request, 'cosmetics_app/suggestions.html', {'type_name': type_name, 'products': good_products})


def ingredients(request):
    all_objects = Ingredient.objects.all()
    return render(request, 'cosmetics_app/ingredients.html', {'all_objects': all_objects})


def cosmetics(request):
    all_objects = Cosmetic.objects.all()
    return render(request, 'cosmetics_app/cosmetics.html', {'all_objects': all_objects})


def functions(request):
    all_objects = Function.objects.all()
    return render(request, 'cosmetics_app/functions.html', {'all_objects': all_objects})


def features(request):
    all_features = Feature.objects.all()
    return render(request, 'cosmetics_app/features.html', {'all_features': all_features})


def types(request):
    all_types = Type.objects.all()
    return render(request, 'cosmetics_app/types.html', {'all_types': all_types})


def brands(request):
    all_brands = Brand.objects.all()
    return render(request, 'cosmetics_app/brands.html', {'all_brands': all_brands})


def create(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('brand') and request.POST.get(
                'type') and request.POST.get('ingredient', ''):
            cosmetic = Cosmetic()
            cosmetic.full_name = request.POST.get('name')

            brand_name = request.POST.get('brand')
            # szuka w bazie odpowiedniego obiektu z klasy Brand aby go pobrac
            bra = Brand.objects.get(name=brand_name)
            bra.save()

            type_name = request.POST.get('type')
            # szuka w bazie odpowiedniego obiektu z klasy Type aby go pobrac
            typ = Type.objects.get(name=type_name)
            typ.save()

            cosmetic.brand = bra
            cosmetic.type = typ
            cosmetic.save()

            ingredients1 = request.POST.get('ingredient', '')
            ingredient_list = ingredients1.split(',')
            for i in ingredient_list:
                ing_1 = i.strip()
                ing = Ingredient.objects.get(INCI=ing_1)
                cosmetic.ingredient.add(ing)

            return render(request, 'cosmetics_app/create.html',
                          {'name': cosmetic.full_name, 'brand': bra.name, 'type': typ.name,
                           'ingredient': ingredients1})

    else:
        return render(request, 'cosmetics_app/create.html')
