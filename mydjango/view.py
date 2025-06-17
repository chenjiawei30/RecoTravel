from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
import urllib.parse
from .sam.main_pro import *
from django.http import JsonResponse, StreamingHttpResponse
import requests
import os
from django.conf import settings
from .sam.seasonal_rec import seasonal_recommend

def travelHome(request):
    return render(request,"index.html")


def spot_choose(request):
    # 从JSON文件加载景点数据
    with open('static/spots.json', 'r', encoding='utf-8') as f:
        spots = json.load(f)
    return render(request, "spot.html", {'spots': spots})


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

def seasonal_spot(request):
    num = int(request.GET.get("num", 6))
    season, names, addrs, _ = seasonal_recommend(num)   
    ctx = {
        "season": season,                 # spring / summer / autumn / winter
        "rec_spots": list(zip(names, addrs)),   # [(name, addr), ...]
    }

    return render(request, "seasonal.html", ctx)

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


def gallery(request):
    page = int(request.GET.get('page', 1))
    items_per_page = 12
    
    with open('static/spots.json', 'r', encoding='utf-8') as f:
        all_spots = json.load(f)
    
    total_items = len(all_spots)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    page_range = range(1, total_pages + 1)  # 添加页码范围
    
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_spots = all_spots[start_index:end_index]

    grouped_spots = [paginated_spots[i:i+4] for i in range(0, len(paginated_spots), 4)]
    
    return render(request, "gallery.html", {
        'grouped_spots': grouped_spots,
        'total_pages': total_pages,
        'current_page': page,
        'page_range': page_range  # 传递页码范围
    })


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


def chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # 从环境变量获取API密钥
            api_key = "sk-Q4tevkNHvccXSa70FqtnxYWJV7Nz2t9nyXbBh82b3F04rx2h"
            if not api_key:
                print("Error: API key not configured")
                return JsonResponse({'error': 'API key not configured'}, status=500)
            
            api_url = "http://api.cipsup.cn/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # 构建系统提示词
            system_prompt = """你是一个专业的北京旅游助手，可以帮助用户：
            1. 规划北京旅游路线
            2. 推荐景点和美食
            3. 解答旅游相关问题
            4. 提供交通和住宿建议
            5. 分享北京历史文化知识
            
            请用专业、友好、简洁的语气回答用户的问题。请不要使用markdown格式返回，直接用文本形式返回。"""
            
            payload = {
                "model": "Qwen2.5-72B-Instruct-GPTQ-Int4",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "max_tokens": 500,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "stream": True
            }
            
            def generate():
                try:
                    print("Sending request to API...")
                    response = requests.post(api_url, headers=headers, json=payload, stream=True)
                    print(f"API Response Status: {response.status_code}")
                    
                    if response.status_code != 200:
                        error_msg = f"API request failed with status {response.status_code}"
                        print(error_msg)
                        try:
                            error_detail = response.json()
                            print(f"Error detail: {error_detail}")
                        except:
                            print(f"Raw response: {response.text}")
                        yield f"data: {json.dumps({'error': error_msg})}\n\n"
                        return
                    
                    for line in response.iter_lines():
                        if line:
                            line = line.decode('utf-8')
                            print(f"Received line: {line}")  # 打印接收到的每一行
                            if line.startswith('data: '):
                                data = line[6:]  # 去掉 "data: " 前缀
                                if data == "[DONE]":
                                    yield f"data: {json.dumps({'done': True})}\n\n"
                                else:
                                    try:
                                        json_data = json.loads(data)
                                        if 'choices' in json_data and len(json_data['choices']) > 0:
                                            delta = json_data['choices'][0].get('delta', {})
                                            if 'content' in delta:
                                                yield f"data: {json.dumps({'content': delta['content']})}\n\n"
                                    except json.JSONDecodeError as e:
                                        print(f"JSON decode error: {e}")
                                        print(f"Problematic data: {data}")
                                        continue
                except Exception as e:
                    print(f"Error in generate function: {str(e)}")
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
            return StreamingHttpResponse(
                generate(),
                content_type='text/event-stream'
            )
            
        except Exception as e:
            print(f"Error in chat_view: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)