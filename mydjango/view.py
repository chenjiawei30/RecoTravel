from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
import urllib.parse
from .sam.main_pro import *


def travelHome(request):
    return render(request,"index.html")


def spot_choose(request):
    return render(request,"spot.html")


def route_show(request):
    return render(request,"route.html")


def route_design(request):
    return render(request,"route_design.html")


def about(request):
    return render(request,"about.html")


def gallery(request):
    return render(request,"gallery.html")


def error404(request):
    return render(request,"404.html")


def blog(request):
    return render(request,"blog.html")


def blog_single(request):
    return render(request,"blog-single.html")


def contact(request):
    return render(request,"contact.html")


def reco(request):
    if request.method == "POST":
        # 解析参数
        raw_data = urllib.parse.unquote(str(request.body,'utf-8'))
        spot_data = raw_data.split('&')
        spot_num = spot_data.pop().lstrip('num=')
        # 错误处理
        if spot_num == "输入景点个数":
            return render(request, "404.html")

        # 取出目标景点个数
        num = int(spot_num)
        print(num)
        # 取出选择的景点
        spot_list = [s.lstrip('spot=') for s in spot_data]
        print(spot_list)
        # 错误处理
        if len(spot_list) == 0:
            return render(request, "404.html")

        # 推荐路线
        route_list = tra_rec(spot_list,num)
        print(route_list)
        # 传给前端
        route = dict()

        route['spot_name'] = route_list[0]

    return render(request,"route.html",route)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')  # 登录成功后直接跳转到首页
        else:
            return render(request, 'login.html', {'error_message': '用户名或密码错误'})
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # 验证密码是否匹配
        if password1 != password2:
            return render(request, 'register.html', {'error_message': '两次输入的密码不匹配'})

        # 验证用户名是否已存在
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': '用户名已存在'})

        # 验证邮箱是否已存在
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': '邮箱已被注册'})

        # 创建新用户
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # 自动登录
        login(request, user)
        return redirect('/')

    return render(request, 'register.html')