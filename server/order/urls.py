from django.urls import path
from . import views

urlpatterns = [
    path('cart/insert/', views.insert_cart_page, name='insert_cart_page'),
    path('cart/update_status/', views.update_status_page, name='update_status_page'),
    path('cart/user_carts', views.get_users_cart_page, name='get_user_carts_page'),
    path('cart/restaurant_carts', views.get_restaurant_carts_page, name='get_restaurant_carts_page'),
    path('cart/decline/', views.decline_cart_page, name='decline_cart_page'),
    path('cart/cancel/', views.cancel_cart_page, name='cancel_cart_page'),
    path('item/insert/', views.insert_item_page, name='insert_item_page'),
    path('item/remove/', views.remove_item_page, name='remove_item_page'),

    path('item/edit_amount', views.edit_item_amount_page, name= 'edit_item_amount_page'),
    path('item/get_by_cart/', views.get_items_by_cart_page, name='edit_item_by_cart_page')
]
