from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

    content = {
        'title': title,
        'basket_items': basket_items,
    }

    return render(request, 'basketapp/basket.html', content)


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product = get_object_or_404(Product, pk=pk)
    basket_item = Basket.objects.filter(user=request.user, product=product).first()

    if not basket_item:
        basket_item = Basket(user=request.user, product=product)

    basket_item.quantity += 1
    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
