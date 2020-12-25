from django.urls import path
from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderListView.as_view(), name='orders_list'),
    path('create/', ordersapp.OrderCreateView.as_view(), name='order_create'),
]
