from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from .models import User, Blog
from utils import uuidUtil
from datetime import datetime
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
import os, json
from django.db import models


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
    # user_name = request.POST['username']
    # password = request.POST['password']
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user_name = body['username']
    password = body['password']
    #
    try:
        user = User.objects.get(user_name=user_name, password=password)
    except User.DoesNotExist:
        res = {'code': 100, 'message': '用户名密码错误'}
        return HttpResponse(json.dumps(res), content_type='application/json')
    # try:
    #     user = get_object_or_404(User, user_name=user_name, password=password)
    # except ValueError:
    #     res = {'errorcode': 100, 'message': '用户名密码错误'}
    #     return HttpResponse(json.dumps(res), content_type='application/json')
        # return HttpResponseRedirect('user/', message='用户名密码错误')
    # if user is None:
    #     return HttpResponseRedirect('user/', message='用户名密码错误')
    # print('here')
    # session的使用
    request.session['name'] = user_name
    request.session['user_id'] = user.user_id
    request.session.set_expiry(None)
    res = {'code': 200, 'message': '登录成功'}
    return HttpResponse(json.dumps(res), content_type='application/json')


class Menu(models.Model):
    menu_id = models.CharField(primary_key=True, max_length=32)
    menu_name = models.CharField(max_length=20)
    menu_order = models.IntegerField()
    menu_level = models.IntegerField()

    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))


def get_menus(request):
    menus = [Menu('erwer', '菜单一', 0, 1)]
    menus.append(Menu('wrewr', '菜单二', 1, 1))
    menus.append(Menu('rwerer', '菜单三', 2, 1))
    data = serializers.serialize('json', menus, ensure_ascii=False)
    res = {'code': 200, 'message': data}
    return HttpResponse(data, content_type='application/json')


def log_out(request):
    del request.session['user_id']
    res = {'code': 200, 'message': '退出成功'}
    return HttpResponse(json.dumps(res), content_type='application/json')


def main_pages(request):
    user_id = request.session.get('user_id', None)
    if user_id:
        return render(request, 'user/main.html')
    else:
        return HttpResponseRedirect('/myblog')


def user_info(request):
    user_id = request.session['user_id']
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            res = {'code': 100, 'message': '用户名密码错误'}
            return HttpResponse(json.dumps(res), content_type='application/json')
        message = {'user': user}
        return render(request, 'user/user_info.html', context=message)
    # model = User
    # template_name = 'user/user_info.html'


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


def blog_list(request):
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 10)
    page = request.POST.get('page', None)
    try:
        blog = paginator.page(page)
    except PageNotAnInteger:
        blog = paginator.page(1)
    except EmptyPage:
        blog = paginator.page(paginator.num_pages)
    return render(request, 'blog/blog_list.html', {'blog_list': blog})

