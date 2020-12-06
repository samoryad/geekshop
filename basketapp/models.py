from django.conf import settings
from django.db import models
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @property
    # метод, считающий количество товаров в корзине пользователя
    def total_quantity(self):
        user_basket_objects = Basket.objects.filter(user=self.user)
        totalquantity = 0
        for object in user_basket_objects:
            totalquantity += object.quantity

        return totalquantity
