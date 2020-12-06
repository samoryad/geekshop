import json
from django.shortcuts import render, get_object_or_404
import datetime
import os
from django.conf import settings

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def main(request):
    title = 'Главная'
    products = Product.objects.all()[:4]
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    print(pk)

    title = 'продукты'
    links_menu = ProductCategory.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

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
            'basket': basket
        }

        return render(request, 'mainapp/products_list.html', content)

    same_products = Product.objects.all()[2:5]

    content = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products
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
    content = {'title': title, 'visit_date': visit_date, 'locations': locations}
    return render(request, 'mainapp/contact.html', content)
