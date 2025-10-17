from django.urls import path
from . import views

# 定义应用命名空间，用于区分不同应用的URL名称
app_name = 'blog'

# URL模式列表，将URL路由映射到相应的视图函数
urlpatterns = [
    # 首页路由，显示所有已发布的文章列表
    path('', views.post_list, name='post_list'),
    
    # 文章详情路由，显示单篇文章的详细内容
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    # 创建文章路由，用于创建新的文章
    path('post/new/', views.post_create, name='post_create'),
    
    # 编辑文章路由，用于编辑已有的文章
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    
    # 删除文章路由，用于删除已有的文章
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
]