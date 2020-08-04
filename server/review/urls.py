from django.urls import path
from . import views

urlpatterns = [
    path('insert/', views.insert_review_page, name='insert_review_page'),
    path('get_by_restaurant/', views.get_restaurant_reviews_page, name='get_restaurant_reviews_page'),

]
