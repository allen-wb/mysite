from django.urls import path
from . import views


app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),
    path('log_in', views.log_in, name='log_in'),
    path('to_register', views.to_register, name='to_register'),
    path('register', views.register, name='register'),
    path('<str:pk>/user_info', views.UserInfoView.as_view(), name='user_info'),
    path('update_user', views.update_user, name='update_user')
]
