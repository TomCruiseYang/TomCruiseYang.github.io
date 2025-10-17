from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    """
    文章模型，用于存储博客文章信息
    """
    # 文章标题，最大长度200字符
    title = models.CharField(max_length=200, verbose_name='标题')
    
    # 文章内容，使用TextField存储长文本
    content = models.TextField(verbose_name='内容')
    
    # 文章作者，关联Django内置User模型，文章删除时级联删除相关文章
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    
    # 文章创建时间，auto_now_add=True表示只在创建时自动设置
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    # 文章更新时间，auto_now=True表示每次保存时自动更新
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 文章发布状态，布尔值，默认为False（草稿状态）
    published = models.BooleanField(default=False, verbose_name='是否发布')
    
    class Meta:
        # 在Django管理后台显示的单数形式名称
        verbose_name = '文章'
        # 在Django管理后台显示的复数形式名称
        verbose_name_plural = '文章'
        # 文章列表的默认排序方式，按创建时间倒序排列
        ordering = ['-created_at']
    
    def __str__(self):
        """
        定义模型实例的字符串表示，返回文章标题
        """
        return self.title
    
    def get_absolute_url(self):
        """
        获取文章的绝对URL，用于在创建或更新文章后重定向
        返回文章详情页面的URL
        """
        return reverse('blog:post_detail', args=[str(self.id)])

class Comment(models.Model):
    """
    评论模型，用于存储文章评论信息
    """
    # 关联的文章，related_name='comments'允许通过post.comments访问文章的所有评论
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    
    # 评论作者，关联Django内置User模型
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    
    # 评论内容，使用TextField存储长文本
    content = models.TextField(verbose_name='评论内容')
    
    # 评论创建时间，auto_now_add=True表示只在创建时自动设置
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    
    class Meta:
        # 在Django管理后台显示的单数形式名称
        verbose_name = '评论'
        # 在Django管理后台显示的复数形式名称
        verbose_name_plural = '评论'
        # 评论列表的默认排序方式，按创建时间正序排列
        ordering = ['created_at']
    
    def __str__(self):
        """
        定义模型实例的字符串表示，返回评论的简要描述
        格式：作者 对 文章标题 的评论
        """
        return f'{self.author.username} 对 {self.post.title} 的评论'
