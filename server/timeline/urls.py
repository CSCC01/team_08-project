from django.urls import path
from . import views

urlpatterns = [
    path('post/upload/', views.upload_post, name='upload_post_page'),
    path('comment/upload/', views.upload_comment, name='upload_comment_page')
]