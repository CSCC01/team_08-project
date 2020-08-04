from django.urls import path
from . import views

urlpatterns = [
    path('insert/', views.insert_review_page, name='insert_review_page'),
    path('get/', views.get_review_page, name='get_review_page'),

]
