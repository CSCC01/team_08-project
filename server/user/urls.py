from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_page, name='signup_page'),
    path('role_reassign/', views.reassign_page, name='reassign_page'),
    path('data/', views.data_page, name='data_page'),
    path('exists/', views.exists_page, name='exists_page'),
]
