from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, \
    get_hebdomad_hot_data
from blogs.models import Blog
from django.core.paginator import Paginator
from django.db.models import Q





def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

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

def search(request):

    search_words = request.GET.get('wd', '')   # 接收前端的wd关键字  也有可能是空的
    # 分词：按空格 & | ~
    condition = None
    for word in search_words.split(' '):  # 将关键字分开
        if condition is None:   # 如果 condition 为空
            condition = Q(title__icontains=word)  # 直接将拆分后的Word赋值 (title__icontains  模糊匹配,加i是不区分大小写)
        else:
            condition = condition | Q(title__icontains=word)   # 如果已经赋值过了就将它合并在一起

    search_blogs = []    # 如果搜索不到
    if condition is not None:   # 如果不存在
        # 筛选：搜索
        search_blogs = Blog.objects.filter(condition)

    # 筛选:搜索
    # search_blogs = Blog.objects.filter(title__icontains=search_words)   # 进行匹配(title__icontains  模糊匹配,加i是不区分大小写)

    # 分页
    paginator = Paginator(search_blogs, 20)  # 将search_blogs分页,20个
    page_num = request.GET.get('page', 1)  # 获取URL的页面参数(get请求)
    page_of_blogs = paginator.get_page(page_num)  # 内置的报错处理 只要是输入的不是int型 会自己默认处理成1

    context = {}
    context['search_words'] = search_words
    context['search_blogs_count'] = search_blogs.count()
    context['page_of_blogs'] = page_of_blogs
    return render(request, 'search.html', context)


