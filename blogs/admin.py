from django.contrib import admin
from .models import BlogType, Blog

# Register your models here.
import pysnooper

# @pysnooper.snoop("blogadmin_debug.log",depth=2)

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type_name")


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', "title", "blog_type", "author", "get_read_num", "created_time", "last_updated_time")




