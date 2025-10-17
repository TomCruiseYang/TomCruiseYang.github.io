from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from utils.logger import logger

def register_view(request):
    """
    用户注册视图函数，处理用户账户创建
    
    参数:
        request (HttpRequest): HTTP请求对象
    
    返回:
        HttpResponse: 渲染后的用户注册表单页面或重定向到登录页面
    """
    if request.method == 'POST':
        # 处理POST请求，即提交注册表单数据
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 表单数据验证通过，创建新用户
            user = form.save()
            # 获取注册的用户名
            username = form.cleaned_data.get('username')
            # 添加成功消息提示
            messages.success(request, f'账号 {username} 创建成功！现在可以登录了。')
            # 重定向到登录页面
            return redirect('accounts:login')
    else:
        # 处理GET请求，即显示空的注册表单
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """
    用户登录视图函数，处理用户身份验证
    
    参数:
        request (HttpRequest): HTTP请求对象
    
    返回:
        HttpResponse: 渲染后的用户登录表单页面或重定向到首页
    """
    # 记录登录视图被访问的日志
    logger.info(f"登录视图被访问, {request}")
    if request.method == 'POST':
        # 处理POST请求，即提交登录表单数据
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 表单数据验证通过，获取用户名和密码
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # 验证用户凭据
            user = authenticate(username=username, password=password)
            if user is not None:
                # 用户验证成功，登录用户
                login(request, user)
                # 添加欢迎消息提示
                messages.info(request, f'欢迎 {username} 登录！')
                # 检查是否有重定向URL参数
                next_url = request.GET.get('next')
                if next_url:
                    # 如果有重定向URL，则跳转到该URL
                    return redirect(next_url)
                else:
                    # 否则重定向到文章列表页面
                    return redirect('blog:post_list')
            else:
                # 用户验证失败，显示错误信息
                messages.error(request, '用户名或密码不正确。')
        else:
            # 表单验证失败，显示错误信息
            messages.error(request, '用户名或密码不正确。')
    else:
        # 处理GET请求，即显示空的登录表单
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    """
    用户登出视图函数，处理用户退出登录，需要用户已登录才能访问
    
    参数:
        request (HttpRequest): HTTP请求对象
    
    返回:
        HttpResponse: 重定向到文章列表页面
    """
    # 退出当前用户登录状态
    logout(request)
    # 添加退出登录消息提示
    messages.info(request, '您已成功退出登录。')
    # 重定向到文章列表页面
    return redirect('blog:post_list')
