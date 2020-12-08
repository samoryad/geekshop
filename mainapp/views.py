import json
import random

from django.shortcuts import render, get_object_or_404
import datetime
import os
from django.conf import settings

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'Главная'
    products = Product.objects.all()[:4]
    content = {'title': title, 'products': products, 'basket': get_basket(request.user)}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    print(pk)

    title = 'продукты'
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category = {'name': 'все', 'pk': 0}
        else:
            # category = ProductCategory.objects.get(pk=pk)
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk).order_by('price')

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_list,
            'basket': get_basket(request.user),
        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'basket': get_basket(request.user),
        'hot_product': hot_product
    }

    return render(request, 'mainapp/products.html', content)


def contact(request):
    title = 'о нас'
    visit_date = datetime.datetime.now()
    # locations = []
    file_path = os.path.join(settings.BASE_DIR, 'mainapp/JSON/contacts.json')
    # или так settings.BASE_DIR / 'contacts.json'
    with open(file_path) as file_contacts:
        # можно так
        # file_content = file_contacts.read()
        # locations = json.loads(file_content)
        # но лучше так:
        locations = json.load(file_contacts)
    content = {'title': title, 'visit_date': visit_date, 'locations': locations, 'basket': get_basket(request.user)}
    return render(request, 'mainapp/contact.html', content)

# обработка ошибки 404
# def not_found(request, exception):
#     # можно внести действия (выборка из базы, преобразование данных и т. д.
#     return render(request, '404.html', context={'item': 'item'}, status=404)
