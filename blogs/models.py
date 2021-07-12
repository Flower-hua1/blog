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
    type_name = models.CharField(max_length=30)   # 博客类型
    def __str__(self):
        return self.type_name

class Blog(models.Model,ReadNumExpandMethod):
    # 博客功能模型s
    title = models.CharField(max_length=50)  # 标题
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    # content = models.TextField()             #文章内容
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # djnago 自带的user

    created_time = models.DateTimeField(auto_now_add=True)   #添加时间
    last_updated_time = models.DateTimeField(auto_now=True)  #更新时间

    def __str__(self):
        # return self.title
        return "<Blog: %s>" % self.title

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    class Meta:
        ordering = ["-created_time"]

