import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    # 检查是否已存在管理员账户
    if User.objects.filter(username='admin').exists():
        print("管理员账户已存在")
        return
    
    # 创建管理员账户
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print(f"管理员账户创建成功: {admin.username}")

if __name__ == '__main__':
    create_admin_user()