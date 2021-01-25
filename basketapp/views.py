from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category').select_related()

    content = {
        'title': title,
        'basket_items': basket_items,
    }

    return render(request, 'basketapp/basket.html', content)

# моя старая версия перед ДЗ №8 (F-объекты)
# @login_required
# def basket_add(request, pk):
#     if 'login' in request.META.get('HTTP_REFERER'):
#         return HttpResponseRedirect(reverse('products:product', args=[pk]))
#     product = get_object_or_404(Product, pk=pk)
#     basket_item = Basket.objects.filter(user=request.user, product=product).first()
#
#     if not basket_item:
#         basket_item = Basket(user=request.user, product=product)
#
#     basket_item.quantity += 1
#     # добавить 'quantity' в скобки при ошибке update_fields
#     # (если будет приходить пустое поле в сигнале product_quantity_update_save)
#     basket_item.save()
#
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)
    old_basket_item = Basket.get_product(user=request.user, product=product)

    if old_basket_item:
        # old_basket_item[0].quantity += 1
        old_basket_item[0].quantity = F('quantity') + 1
        old_basket_item[0].save()

        # для просмотра разницы в верхнем коде
        # update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
        # print(f'query basket_add: {update_queries}')
    else:
        new_basket_item = Basket(user=request.user, product=product)
        new_basket_item.quantity += 1
        new_basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove_ajax(request, pk):
    if request.is_ajax():
        basket_for_delete = Basket.objects.get(pk=pk)
        basket_for_delete.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})
