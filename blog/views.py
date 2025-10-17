from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Post
from .forms import PostForm

def post_list(request):
    """
    显示所有已发布的文章列表视图函数
    
    参数:
        request (HttpRequest): HTTP请求对象
    
    返回:
        HttpResponse: 渲染后的文章列表页面
    """
    # 只显示已发布的文章，过滤掉草稿状态的文章
    posts = Post.objects.filter(published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    """
    显示单篇文章详细内容的视图函数
    
    参数:
        request (HttpRequest): HTTP请求对象
        pk (int): 文章的主键ID
    
    返回:
        HttpResponse: 渲染后的文章详情页面或403错误页面
    """
    # 获取指定ID的文章对象，如果不存在则返回404错误
    post = get_object_or_404(Post, pk=pk)
    # 只允许查看已发布的文章，除非是作者自己访问
    if not post.published and post.author != request.user:
        # 如果用户没有权限查看文章，返回403错误
        return HttpResponseForbidden("您没有权限查看这篇文章。")
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    """
    创建新文章的视图函数，需要用户登录才能访问
    
    参数:
        request (HttpRequest): HTTP请求对象
    
    返回:
        HttpResponse: 渲染后的文章创建表单页面或重定向到文章详情页面
    """
    if request.method == 'POST':
        # 处理POST请求，即提交表单数据
        form = PostForm(request.POST)
        if form.is_valid():
            # 表单数据验证通过，保存文章但不立即提交到数据库
            post = form.save(commit=False)
            # 设置文章作者为当前登录用户
            post.author = request.user
            # 保存文章到数据库
            post.save()
            # 添加成功消息提示
            messages.success(request, '文章创建成功！')
            # 重定向到新创建的文章详情页面
            return redirect('blog:post_detail', pk=post.pk)
        else:
            # 表单验证失败，显示错误信息
            messages.error(request, '表单验证失败，请检查输入内容。')
    else:
        # 处理GET请求，即显示空表单
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'title': '创建文章'})

@login_required
def post_edit(request, pk):
    """
    编辑文章的视图函数，需要用户登录才能访问
    
    参数:
        request (HttpRequest): HTTP请求对象
        pk (int): 要编辑的文章主键ID
    
    返回:
        HttpResponse: 渲染后的文章编辑表单页面或重定向到文章详情页面
    """
    # 获取指定ID的文章对象，如果不存在则返回404错误
    post = get_object_or_404(Post, pk=pk)
    # 检查权限：只有文章作者可以编辑
    if post.author != request.user:
        # 如果用户没有权限编辑文章，返回403错误
        return HttpResponseForbidden("您没有权限编辑这篇文章。")
    
    if request.method == 'POST':
        # 处理POST请求，即提交表单数据
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # 表单数据验证通过，保存文章但不立即提交到数据库
            post = form.save(commit=False)
            # 保存文章到数据库
            post.save()
            # 添加成功消息提示
            messages.success(request, '文章更新成功！')
            # 重定向到更新后的文章详情页面
            return redirect('blog:post_detail', pk=post.pk)
        else:
            # 表单验证失败，显示错误信息
            messages.error(request, '表单验证失败，请检查输入内容。')
    else:
        # 处理GET请求，即显示包含文章当前内容的表单
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'title': '编辑文章'})

@login_required
def post_delete(request, pk):
    """
    删除文章的视图函数，需要用户登录才能访问
    
    参数:
        request (HttpRequest): HTTP请求对象
        pk (int): 要删除的文章主键ID
    
    返回:
        HttpResponse: 渲染后的删除确认页面或重定向到文章列表页面
    """
    # 获取指定ID的文章对象，如果不存在则返回404错误
    post = get_object_or_404(Post, pk=pk)
    # 检查权限：只有文章作者可以删除
    if post.author != request.user:
        # 如果用户没有权限删除文章，返回403错误
        return HttpResponseForbidden("您没有权限删除这篇文章。")
    
    if request.method == 'POST':
        # 处理POST请求，即确认删除操作
        post.delete()
        # 添加成功消息提示
        messages.success(request, '文章删除成功！')
        # 重定向到文章列表页面
        return redirect('blog:post_list')
    
    # 处理GET请求，显示删除确认页面
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
