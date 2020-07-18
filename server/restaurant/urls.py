from django.urls import path

from . import views

urlpatterns = [
    path('tag/insert/', views.insert_tag_page, name='insert_tag_page'),
    path('tag/clear/', views.clear_tags_page, name='clear_tags_page'),
    path('tag/auto/', views.auto_tag_page, name='auto_tag_page'),
    path('dish/insert/', views.insert_dish_page, name='insert_dish_page'),
    path('dish/get_all/', views.all_dishes_page, name='all_dishes_page'),
    path('dish/get_by_restaurant/', views.get_dish_by_restaurant_page, name='get_dish_by_restaurant_page'),
    path('get/', views.get_restaurant_page, name='get_restaurant_page'),
    path('insert/', views.insert_restaurant_page, name='insert_restaurant_page'),
    path('get_all/', views.get_all_restaurants_page, name='get_all_restaurants_page'),
    path('edit/', views.edit_restaurant_page, name='edit_restaurant_page')
]
