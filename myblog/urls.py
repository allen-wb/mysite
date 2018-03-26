from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('main_pages', views.main_pages, name='main_pages'),
]
