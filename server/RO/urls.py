from django.urls import path

from . import views

urlpatterns = [
    path('get/', views.get, name='get'),
    path('insert/', views.insert, name='insert'),
    path('getAll/', views.get_all, name='get_all'),
    path('upload_logo/', views.update_logo, name='upload_logo')
]
