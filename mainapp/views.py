import json
from django.shortcuts import render
import datetime
import os
from django.conf import settings
from mainapp.models import Product, ProductCategory


def main(request):
    title = 'Главная'
    products = Product.objects.all()[:4]
    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    print(pk)
    links_menu = ProductCategory.objects.all()
    content = {
        'title': 'Продукты',
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', content)


def products_classic(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'Продукты',
        'links_menu': links_menu
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
