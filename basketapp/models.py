from django.conf import settings
from django.db import models
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @property
    # метод вычисления общей цены одинаковых продуктов
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    # метод, считающий количество товаров в корзине пользователя
    def total_quantity(self):
        _user_basket_objects = Basket.objects.filter(user=self.user)
        _total_quantity = sum(list(map(lambda x: x.quantity, _user_basket_objects)))
        return _total_quantity

    @property
    # метод вычисления общей стоимости продуктов конкретного пользователя
    def total_cost(self):
        _user_basket_objects = Basket.objects.filter(user=self.user)
        _total_cost = sum(list(map(lambda x: x.product_cost, _user_basket_objects)))
        return _total_cost
