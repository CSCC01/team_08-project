from django.urls import path
from . import views

urlpatterns = [
    path('post/upload/', views.upload_post_page, name='upload_post_page'),
    path('post/get_all/', views.get_all_posts_page, name='get_all_posts_page'),
    path('comment/upload/', views.upload_comment_page, name='upload_comment_page')
]