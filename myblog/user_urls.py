from django.urls import path
from . import views


app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),
    path('log_in', views.log_in, name='log_in'),
    path('log_out', views.log_out, name='log_out'),
    path('to_register', views.to_register, name='to_register'),
    path('register', views.register, name='register'),
    path('user_info', views.user_info, name='user_info'),
    path('update_user', views.update_user, name='update_user'),
    path('blog_list', views.blog_list, name='blog_list'),
    path('get_menus', views.get_menus, name='get_menus')
]
