from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),
    # Для кеширования всей страницы нужно добавить cache_page(3600)() перед контроллером, например mainapp.products
    path('category/<int:pk>/', mainapp.products, name='category'),
    path('category/<int:pk>/<page>/', mainapp.products, name='page'),
    path('product/<int:pk>/', mainapp.product, name='product'),
]
