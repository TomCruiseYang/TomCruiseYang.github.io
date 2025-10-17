import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post

def test_blog_functionality():
    print("开始测试博客应用功能...")
    
    # 创建测试用户
    if not User.objects.filter(username='testuser').exists():
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        print(f"创建测试用户: {user.username}")
    else:
        user = User.objects.get(username='testuser')
        print(f"使用现有测试用户: {user.username}")
    
    # 创建测试文章
    if not Post.objects.filter(title='测试文章').exists():
        post = Post.objects.create(
            title='测试文章',
            content='这是一篇用于测试的文章内容。',
            author=user,
            published=True
        )
        print(f"创建测试文章: {post.title}")
    else:
        post = Post.objects.get(title='测试文章')
        print(f"使用现有测试文章: {post.title}")
    
    # 测试文章查询
    posts = Post.objects.all()
    print(f"数据库中共有 {posts.count()} 篇文章")
    
    # 测试文章详情
    post_detail = Post.objects.get(pk=post.pk)
    print(f"文章详情 - 标题: {post_detail.title}, 作者: {post_detail.author.username}")
    
    # 测试文章更新
    post.title = '更新后的测试文章'
    post.save()
    print(f"文章已更新为: {post.title}")
    
    print("所有功能测试完成！")

if __name__ == '__main__':
    test_blog_functionality()