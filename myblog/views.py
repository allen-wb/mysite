from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponseRedirect
from django.views import generic
from .models import User
from utils import uuidUtil
from datetime import datetime
from django.conf import settings
import os


# Create your views here.
def index(request):
    return render(request, 'user/index.html')


def to_register(request):
    return render(request, 'user/user_register.html')


def register(request):
    true_name = request.POST['true_name']
    user_name = request.POST['user_name']
    password = request.POST['password']
    tel = request.POST['tel']
    email = request.POST['email']
    user = User(user_id=uuidUtil.get_uuid(), true_name=true_name,
                user_name=user_name, password=password, tel=tel,
                email=email, create_date=datetime.now(), creater='',
                sex=1, age=25, image='', address='', is_delete=0,
                update_date=datetime.now(), updater='', remark='')
    user.save()
    return HttpResponseRedirect('/myblog')


def log_in(request):
    user_name = request.POST['user_name']
    password = request.POST['password']
    #
    try:
        user = get_object_or_404(User, user_name=user_name, password=password)
    except ValueError:
        return HttpResponseRedirect('user/', message='用户名密码错误')
    # if user is None:
    #     return HttpResponseRedirect('user/', message='用户名密码错误')
    # print('here')
    # session的使用
    request.session['name'] = user_name
    request.session['user_id'] = user.user_id
    return HttpResponseRedirect('/myblog/' + user.user_id + '/user_info')


class UserInfoView(generic.DetailView):
    model = User
    template_name = 'user/user_info.html'


def update_user(request):
    # 从session中获取信息
    user_id = request.session['user_id']
    if user_id:
        pass
    image = request.FILES.get('image', None)  # 获取前端传过来的文件
    if image:
        file_root = settings.MEDIA_ROOT  # 获取上传路径，在settings配置好的
        if not os.path.isdir(file_root):
            os.mkdir(file_root)
        upload_file = '%s%s' % (file_root, image.name)
        with open(upload_file, 'wb') as new_file:
            for chunk in image.chunks():
                new_file.write(chunk)

    sex = request.POST['sex']
    age = request.POST['age']
    user_id = request.POST['user_id']
    user = get_object_or_404(User, pk=user_id)
    user.image = image
    user.sex = sex
    user.age = age
    user.save()
    return HttpResponseRedirect('/myblog/' + user.user_id + '/user_info')

