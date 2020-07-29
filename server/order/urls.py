from django.urls import path
from . import views

urlpatterns = [
    path('cart/insert/', views.insert_cart_page, name='insert_cart_page'),
    path('item/insert/', views.insert_item_page, name='insert_item_page'),
]
