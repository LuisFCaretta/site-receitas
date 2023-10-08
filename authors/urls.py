from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register_view'),
    path('register/create/', views.register_create, name='create'),
]
