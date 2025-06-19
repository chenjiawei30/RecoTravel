from django.shortcuts import render,HttpResponse, redirect, get_object_or_404
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
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
from .sam.seasonal_rec import seasonal_recommend
from .models import Comment, Post
from django.utils import timezone
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib import messages
from django.urls import reverse
import re

# 加载.env文件
load_dotenv()

        
def clean_title(title):
    # 移除序号、标点和空白字符
    return re.sub(r'^[0-9\.\s、]+', '', title).strip()

def travelHome(request):
    return render(request,"index.html")

def route_design(request):
    return render(request,"route_design.html")


def about(request):
    return render(request,"about.html")


def gallery(request):
    return render(request,"gallery.html")


def error404(request):
    return render(request,"404.html")

def recommend_view(request):
    if request.method == 'POST':
        # 获取用户输入关键词
        keywords = request.POST.get('keywords', '')

        file_path = os.path.join(settings.BASE_DIR, 'static', 'spots.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            spots = json.load(f)
        
        # 调用大模型API进行推荐
        # 这里以通用API调用为例，你需要替换为实际使用的大模型API
        api_url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.LLM_API_KEY}'
        }
        
        # 构建提示词 - 增加格式约束
        prompt = f"根据用户关键词'{keywords}'，从以下景点中推荐3个最匹配的景点。"
        prompt += "要求：只返回景点标题，每个标题占一行，不要解释和额外内容。"
        prompt += f"可选景点：{[spot['title'] for spot in spots]}"
        
        data = {
            'model': 'glm-4-flash-250414',  # 修正为示例中的模型
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 12000  # 增加最大 tokens 参数
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            # 修正分割方式并过滤空行
            recommended_titles = [
                title.strip() for title in response.json()['choices'][0]['message']['content'].split('\n')
                if title.strip()
            ]
        
            recommended_titles = [clean_title(title) for title in recommended_titles if clean_title(title)]
        except Exception as e:
            # 记录错误日志
            print(f"错误: {str(e)}")
            # 返回空推荐结果并提示错误
            return render(request, 'recommendation.html', {
                'spots': [], 
                'keywords': keywords,
                'error': f'推荐服务错误: {str(e)}'
            })
        
        # 筛选推荐的景点详细信息
        recommended_spots = [spot for spot in spots if spot['title'] in recommended_titles]
        return render(request, 'recommendation.html', {'spots': recommended_spots, 'keywords': keywords})
    return render(request, 'recommendation.html')

def blog(request):
    posts = Post.objects.all().order_by('-created_at')
    for post in posts:
        post.comment_count = post.comments.count()
    return render(request, 'blog.html', {'posts': posts})


def blog_single(request):
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f'/login/?next=blog-single.html?post_id={post_id}')
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, username=request.user.username, content=content, created_at=timezone.now())
    comments = post.comments.order_by('-created_at')
    comment_count = comments.count()
    return render(request, 'blog-single.html', {'post': post, 'comments': comments, 'comment_count': comment_count})


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

        # 用户名只能为英文且不超过6个字符
        if not username.isalpha() or not username.isascii() or len(username) > 6:
            return render(request, 'register.html', {'error_message': '用户名只能为英文且不超过6个字符'})

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


@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # 从环境变量获取API key
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print("Error: OPENAI_API_KEY not found in environment variables")
                return JsonResponse({'error': 'API key not configured'}, status=500)
            
            # 实验室内部搭建API网址
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
                # 使用千问72B大模型
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

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.user:
        messages.error(request, '你只能删除自己的评论！')
        return redirect(f"{reverse('blog_single')}?post_id={comment.post.id}")
    if request.method == 'POST':
        comment.delete()
        messages.success(request, '评论已删除！')
    return redirect(f"{reverse('blog_single')}?post_id={comment.post.id}")

@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if title and content:
            post = Post.objects.create(title=title, content=content, author=request.user, image=image)
            return redirect('blog')
    return render(request, 'post_create.html')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        messages.error(request, '你只能删除自己的帖子！')
        return redirect('blog')
    if request.method == 'POST':
        post.delete()
        messages.success(request, '帖子已删除！')
        return redirect('blog')
    return redirect('blog_single')