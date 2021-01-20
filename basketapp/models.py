from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product

# можно создать менеджер (в данном случае из-за удаления QuerySet в ordersapp\views.py
# будет восстановлено количество товаров на складе)
# он обрабатывает не один объект, а сразу пачку объектов - QuerySet)
# class BasketQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#
#         super().delete(*args, **kwargs)


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @property
    # метод вычисления общей цены одинаковых продуктов
    def product_cost(self):
        return self.product.price * self.quantity

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    # метод, считающий количество товаров в корзине пользователя
    def total_quantity(self):
        _user_basket_objects = self.get_items_cached
        _total_quantity = sum(list(map(lambda x: x.quantity, _user_basket_objects)))
        return _total_quantity

    @property
    # метод вычисления общей стоимости продуктов конкретного пользователя
    def total_cost(self):
        _user_basket_objects = self.get_items_cached
        _total_cost = sum(list(map(lambda x: x.product_cost, _user_basket_objects)))
        return _total_cost

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category')

    @staticmethod
    def get_product(user, product):
        return Basket.objects.filter(user=user, product=product)

    @classmethod
    def get_products_quantity(cls, user):
        basket_items = cls.get_items(user)
        basket_items_dic = {}
        [basket_items_dic.update({item.product: item.quantity} for item in basket_items)]

        return basket_items_dic

    # переопределение метода удаления корзинок, будет работать в связке с basket_items[num].delete()
    # из ordersapp\views.py класса OrderCreateView
    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
