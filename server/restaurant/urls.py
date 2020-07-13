from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.add_tag_page, name='add_tag_page'),
    path('clear/', views.clear_tags_page, name='clear_tags_page'),
    path('create/', views.create_dish_page, name='create_dish_page'),
    path('get_all/', views.all_dishes_page, name='all_dishes_page'),
    path('get_food_by_restaurant/', views.get_food_by_restaurant_page, name='get_food_by_restaurant_page'),
    path('auto_tag/', views.auto_tag, name='auto_tag')
]
