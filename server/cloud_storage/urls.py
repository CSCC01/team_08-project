from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.media_upload_page, name='upload_page')
]