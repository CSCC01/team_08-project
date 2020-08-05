from django.urls import path
from . import views

urlpatterns = [
    path('post/upload/', views.upload_post_page, name='upload_post_page'),
    path('post/get_by_restaurant/', views.get_post_by_restaurant_page, name='get_post_by_restaurant_page'),
    path('post/delete/', views.delete_post_page, name='post_delete_page'),
    path('post/get_all/', views.get_all_posts_page, name='get_all_posts_page'),
    path('comment/upload/', views.upload_comment_page, name='upload_comment_page'),
    path('comment/delete/', views.delete_comment_page, name='delete_comment_page'),
    path('comment/get/', views.get_comment_data_page, name='get_comment_data_page')
]
