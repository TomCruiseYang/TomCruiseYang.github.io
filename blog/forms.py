from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    文章表单，用于创建和编辑文章的表单类
    继承自Django的ModelForm，与Post模型关联
    """
    class Meta:
        # 指定关联的模型
        model = Post
        # 指定表单包含的字段
        fields = ['title', 'content', 'published']
        # 为表单字段定义HTML属性和CSS类
        widgets = {
            # 标题字段使用TextInput控件，并添加Bootstrap样式
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入文章标题'
            }),
            # 内容字段使用Textarea控件，并添加Bootstrap样式
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '请输入文章内容'
            }),
            # 发布状态字段使用CheckboxInput控件，并添加Bootstrap样式
            'published': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_title(self):
        """
        自定义标题字段验证方法
        验证标题长度是否符合要求
        
        返回:
            str: 验证通过的标题字符串
            
        异常:
            forms.ValidationError: 当标题长度不符合要求时抛出验证错误
        """
        # 获取清理后的标题数据
        title = self.cleaned_data['title']
        # 验证标题长度不能少于5个字符
        if len(title) < 5:
            raise forms.ValidationError("标题至少需要5个字符")
        # 验证标题长度不能超过200个字符
        if len(title) > 200:
            raise forms.ValidationError("标题不能超过200个字符")
        # 返回验证通过的标题
        return title
    
    def clean_content(self):
        """
        自定义内容字段验证方法
        验证内容长度是否符合要求
        
        返回:
            str: 验证通过的内容字符串
            
        异常:
            forms.ValidationError: 当内容长度不符合要求时抛出验证错误
        """
        # 获取清理后的内容数据
        content = self.cleaned_data['content']
        # 验证内容长度不能少于10个字符
        if len(content) < 10:
            raise forms.ValidationError("文章内容至少需要10个字符")
        # 返回验证通过的内容
        return content