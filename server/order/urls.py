from django.urls import path
from . import views

urlpatterns = [
    path('cart/insert/', views.insert_cart_page, name='insert_cart_page'),
    path('cart/update_status/', views.update_status_page, name='update_status_page'),
    path('cart/cancel/', views.cancel_cart_page, name='cancel_cart_page'),
    path('item/insert/', views.insert_item_page, name='insert_item_page'),
    path('item/remove/', views.remove_item_page, name='remove_item_page'),
    path('item/edit_amount', views.edit_item_amount_page, name='edit_item_amount_page')
]
