from django.urls import path
from . import views

# 定义应用命名空间，用于区分不同应用的URL名称
app_name = 'accounts'

# URL模式列表，将URL路由映射到相应的视图函数
urlpatterns = [
    # 用户注册路由
    path('register/', views.register_view, name='register'),
    
    # 用户登录路由
    path('login/', views.login_view, name='login'),
    
    # 用户登出路由
    path('logout/', views.logout_view, name='logout'),
]