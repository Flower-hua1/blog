from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod
from django.urls import reverse

# Create your models here.
import pysnooper

# @pysnooper.snoop("blog_debug.log",depth=2)




class BlogType(models.Model):
    #博客类型模型
    type_name = models.CharField(max_length=30, verbose_name="博客类型")   # 博客类型
    def __str__(self):
        return self.type_name
    class Meta:
        verbose_name = '博客类型'
        verbose_name_plural = verbose_name

class Blog(models.Model,ReadNumExpandMethod):
    # 博客功能模型s
    title = models.CharField(max_length=50, verbose_name="标题")  # 标题
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, verbose_name="博客类型")
    # content = models.TextField()             #文章内容
    content = RichTextUploadingField(verbose_name="博客内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")  # djnago 自带的user

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")   #添加时间
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")  #更新时间

    def __str__(self):
        # return self.title
        return "<Blog: %s>" % self.title

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_user(self):
        return self.author  # 返回作者本身

    def get_email(self):
        return self.author.email

    class Meta:
        ordering = ["-created_time"]
        verbose_name = '博客'
        verbose_name_plural = verbose_name




