from django import forms
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from ckeditor.widgets import CKEditorWidget
from comment.models import Comment

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                           error_messages={'required': '评论内容不能为空'})

    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': "reply_comment_id"}))  # 创建一个回复评论的ID  不可见



    def __init__(self, *args, **kwargs):
        """
        实例化方法
        继承CommentForm   #父类
        """
        if 'user' in kwargs:   # 判断传入的用户是否在参数里面
            self.user = kwargs.pop('user')   # 获取user
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user  # 如果是登录的就将user给cleaned_data以供我们使用
        else:
            raise forms.ValidationError('用户未登录')  # 前端不可信原则,前端验证后后端也要验证
        # 评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects. \
                get(model=content_type).model_class()  # 得到具体博客的类型 model_class(得到具体的模型对象) 这里做的评论方法是  可以对任何类的对象进行评论
            model_obj = model_class.objects.get(pk=object_id)  # 根据上面找到的博客类型然后在根据ID找到具体的某一篇博客
            self.cleaned_data['content_object'] = model_obj  # 将ID保存到列表里给评论函数调用(comment.views.py)
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')
        return self.cleaned_data


    def clean_reply_comment_id(self):
        # 回复验证  reply_comment_id只有最高级别评论(0),评论的回复,两种
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():  # 判断被回复的评论ID是否存在
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)   # 存在就直接取出赋值
        else:
            raise forms.ValidationError('回复出错')
        return reply_comment_id
