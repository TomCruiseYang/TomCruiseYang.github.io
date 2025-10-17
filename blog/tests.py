from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class BlogTests(TestCase):
    """
    博客应用测试类
    包含对博客文章的列表、详情、创建、更新和删除功能的测试
    """
    
    def setUp(self):
        """
        测试初始化方法，在每个测试方法执行前运行
        创建测试用户、测试文章和测试客户端
        """
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # 创建测试文章
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        
        # 创建测试客户端
        self.client = self.client
    
    def test_post_list_view(self):
        """
        测试文章列表视图
        验证列表页面是否能正确显示文章并返回200状态码
        """
        # 获取文章列表页面的响应
        response = self.client.get(reverse('blog:post_list'))
        # 验证响应状态码为200(成功)
        self.assertEqual(response.status_code, 200)
        # 验证响应中包含文章标题
        self.assertContains(response, 'Test Post')
        # 验证使用的模板正确
        self.assertTemplateUsed(response, 'blog/post_list.html')
    
    def test_post_detail_view(self):
        """
        测试文章详情视图
        验证详情页面是否能正确显示文章内容并返回200状态码
        """
        # 获取文章详情页面的响应
        response = self.client.get(reverse('blog:post_detail', args=[self.post.pk]))
        # 验证响应状态码为200(成功)
        self.assertEqual(response.status_code, 200)
        # 验证响应中包含文章标题和内容
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'Test content')
        # 验证使用的模板正确
        self.assertTemplateUsed(response, 'blog/post_detail.html')
    
    def test_post_create_view(self):
        """
        测试文章创建视图
        验证登录用户能否成功创建新文章
        """
        # 使用测试用户登录
        self.client.login(username='testuser', password='testpass123')
        # 发送POST请求创建新文章
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'New Post',
            'content': 'New content',
        })
        # 验证重定向到文章详情页面
        self.assertEqual(response.status_code, 302)
        # 验证数据库中新增了一篇文章
        self.assertEqual(Post.objects.count(), 2)
        # 验证新文章的标题正确
        self.assertEqual(Post.objects.last().title, 'New Post')
    
    def test_post_update_view(self):
        """
        测试文章更新视图
        验证文章作者能否成功更新自己的文章
        """
        # 使用测试用户登录
        self.client.login(username='testuser', password='testpass123')
        # 发送POST请求更新文章
        response = self.client.post(reverse('blog:post_edit', args=[self.post.pk]), {
            'title': 'Updated Post',
            'content': 'Updated content',
        })
        # 验证重定向到文章详情页面
        self.assertEqual(response.status_code, 302)
        # 重新获取文章对象以获取更新后的数据
        self.post.refresh_from_db()
        # 验证文章标题和内容已更新
        self.assertEqual(self.post.title, 'Updated Post')
        self.assertEqual(self.post.content, 'Updated content')
    
    def test_post_delete_view(self):
        """
        测试文章删除视图
        验证文章作者能否成功删除自己的文章
        """
        # 使用测试用户登录
        self.client.login(username='testuser', password='testpass123')
        # 发送POST请求删除文章
        response = self.client.post(reverse('blog:post_delete', args=[self.post.pk]))
        # 验证重定向到文章列表页面
        self.assertEqual(response.status_code, 302)
        # 验证数据库中文章数量减少
        self.assertEqual(Post.objects.count(), 0)
