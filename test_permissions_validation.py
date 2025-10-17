import os
import django
from django.core.exceptions import ValidationError

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post
from blog.forms import PostForm

def test_data_validation():
    print("开始测试数据验证功能...")
    
    # 测试标题过短的情况
    form_data_short_title = {
        'title': '短',  # 少于5个字符
        'content': '这是一个内容足够长的文章，用来测试表单验证功能。',
        'published': True
    }
    
    form = PostForm(data=form_data_short_title)
    if not form.is_valid():
        print("✓ 标题过短验证成功:", form.errors.get('title'))
    else:
        print("✗ 标题过短验证失败")
    
    # 测试标题过长的情况
    form_data_long_title = {
        'title': 'A' * 201,  # 超过200个字符
        'content': '这是一个内容足够长的文章，用来测试表单验证功能。',
        'published': True
    }
    
    form = PostForm(data=form_data_long_title)
    if not form.is_valid():
        print("✓ 标题过长验证成功:", form.errors.get('title'))
    else:
        print("✗ 标题过长验证失败")
    
    # 测试内容过短的情况
    form_data_short_content = {
        'title': '合适的标题',
        'content': '短内容',  # 少于10个字符
        'published': True
    }
    
    form = PostForm(data=form_data_short_content)
    if not form.is_valid():
        print("✓ 内容过短验证成功:", form.errors.get('content'))
    else:
        print("✗ 内容过短验证失败")
    
    # 测试合法数据
    form_data_valid = {
        'title': '这是一个合适的标题',
        'content': '这是足够长的内容，用来测试表单验证功能。内容需要至少十个字符才能通过验证。',
        'published': True
    }
    
    form = PostForm(data=form_data_valid)
    if form.is_valid():
        print("✓ 合法数据验证成功")
    else:
        print("✗ 合法数据验证失败:", form.errors)
    
    print("数据验证测试完成！\n")

def test_permissions():
    print("开始测试权限控制功能...")
    
    # 创建两个测试用户
    if not User.objects.filter(username='author').exists():
        author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='authorpass123'
        )
        print(f"创建作者用户: {author.username}")
    else:
        author = User.objects.get(username='author')
    
    if not User.objects.filter(username='other_user').exists():
        other_user = User.objects.create_user(
            username='other_user',
            email='other@example.com',
            password='otherpass123'
        )
        print(f"创建普通用户: {other_user.username}")
    else:
        other_user = User.objects.get(username='other_user')
    
    # 创建测试文章
    if not Post.objects.filter(title='权限测试文章').exists():
        post = Post.objects.create(
            title='权限测试文章',
            content='这篇用于测试权限控制的文章内容。',
            author=author,
            published=True
        )
        print(f"创建测试文章: {post.title}")
    else:
        post = Post.objects.get(title='权限测试文章')
        print(f"使用现有测试文章: {post.title}")
    
    # 检查作者是否有权限编辑自己的文章
    if post.author == author:
        print("✓ 文章作者有权编辑自己的文章")
    else:
        print("✗ 文章作者无权编辑自己的文章")
    
    # 检查其他用户是否有权限编辑他人文章
    if post.author != other_user:
        print("✓ 其他用户无权编辑他人的文章")
    else:
        print("✗ 其他用户竟然可以编辑他人的文章")
    
    print("权限控制测试完成！")

if __name__ == '__main__':
    test_data_validation()
    test_permissions()