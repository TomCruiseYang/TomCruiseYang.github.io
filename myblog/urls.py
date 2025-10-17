"""
URL configuration for myblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# URL模式列表，将URL路由映射到相应的视图函数
urlpatterns = [
    # Django管理后台路由
    path('admin/', admin.site.urls),
    
    # 账户应用的URL路由，包含注册、登录、登出功能
    path('accounts/', include('accounts.urls')),
    
    # 博客应用的URL路由，处理文章相关的所有功能
    path('', include('blog.urls')),
]
