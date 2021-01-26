import json
import random

from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
import datetime
import os
from django.conf import settings
from django.views.decorators.cache import cache_page, never_cache

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     return []


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = get_products()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    title = 'Главная'
    # products = Product.objects.all()[:4]
    products = get_products()[:3]
    content = {'title': title, 'products': products, }
    return render(request, 'mainapp/index.html', content)


# можно закэшировать страницу здесь, а можно в urls
# @cache_page(3600)
# сейчас же, наоборот эта страница не будет закеширована, т. к. прописали кеширование всего сайта, а чтобы
# менялся обновляемый контент, ставим never_cache
def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = get_links_menu()

    if pk is not None:
        if pk == 0:
            products_list = get_products_ordered_by_price()
            category = {'name': 'все', 'pk': 0}
        else:
            # category = ProductCategory.objects.get(pk=pk)
            category = get_category(pk)
            products_list = get_products_in_category_ordered_by_price(pk)
            # для получения или или нужно использовать Q объекты
            # products_list = Product.objects.filter(Q(category__name='офис') | Q(category__name=1))

        paginator = Paginator(products_list, 2)
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': product_paginator,
        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
        'hot_product': hot_product
    }

    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    title = 'продукты'
    content = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': get_product(pk),
    }
    return render(request, 'mainapp/product.html', content)


def contact(request):
    title = 'о нас'
    visit_date = datetime.datetime.now()
    # locations = []
    file_path = os.path.join(settings.BASE_DIR, 'mainapp/json/contacts.json')
    # или так settings.BASE_DIR / 'contacts.json'
    with open(file_path) as file_contacts:
        # можно так
        # file_content = file_contacts.read()
        # locations = json.loads(file_content)
        # но лучше так:
        locations = json.load(file_contacts)
    content = {'title': title, 'visit_date': visit_date, 'locations': locations, }
    return render(request, 'mainapp/contact.html', content)

# обработка ошибки 404
# def not_found(request, exception):
#     # можно внести действия (выборка из базы, преобразование данных и т. д.
#     return render(request, '404.html', context={'item': 'item'}, status=404)
