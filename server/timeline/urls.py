from django.urls import path
from . import views

urlpatterns = [
    path('post/upload/', views.upload_post_page, name='upload_post_page'),
    path('post/delete/',views.delete_post_page, name = 'post_delete_page'),
    path('comment/upload/', views.upload_comment_page, name='upload_comment_page')
]