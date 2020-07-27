from django.urls import path
from . import views

urlpatterns = [
    path('post/upload/', views.upload_post_page, name='upload_post_page'),
    path('post/get_by_restaurant/', views.get_post_by_restaurant_page, name='get_post_by_restaurant_page'),
    path('comment/upload/', views.upload_comment_page, name='upload_comment_page')
]
