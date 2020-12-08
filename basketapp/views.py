from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    pass


def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket_item = Basket.objects.filter(user=request.user, product=product).first()

    if not basket_item:
        basket_item = Basket(user=request.user, product=product)

    basket_item.quantity += 1
    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request):
    pass
