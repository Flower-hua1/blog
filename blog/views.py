from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from read_statistics.utils import get_seven_days_read_date, get_today_hot_data, get_yesterday_hot_data, \
    get_hebdomad_hot_data
from blogs.models import Blog


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_date(blog_content_type)

    # 获取7天热门博客缓存数据
    hot_blogs_for_hebdomads = cache.get("hot_blogs_for_hebdomad")  # 取出缓存里的热门博客
    if hot_blogs_for_hebdomads is None:  # 判断缓存中是不是空的
        hot_blogs_for_hebdomad = get_hebdomad_hot_data(blog_content_type)  # 将七天的热门博客取出
        cache.set("hot_blogs_for_hebdomad", hot_blogs_for_hebdomad, 3600)  # 将七天的博客存入缓存
    #     print("1")
    # else:
    #     print(hot_blogs_for_hebdomads[0].object_id)
    #     print("2")
    context = {}
    context["dates"] = dates
    context["read_nums"] = read_nums
    context["today_hot_data"] = get_today_hot_data(blog_content_type)
    context["get_yesterday_hot_data"] = get_yesterday_hot_data(blog_content_type)
    context["hot_blogs_for_hebdomad"] = get_hebdomad_hot_data(blog_content_type)
    return render(request, "home.html", context)





