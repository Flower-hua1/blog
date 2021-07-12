from django.shortcuts import get_object_or_404,render
from django.core.paginator import Paginator
from .models import Blog, BlogType
from django.db.models import Count
from django.conf import settings
from read_statistics.utils import read_statistics_once_read
from user.forms import LoginForms
# Create your views here.


def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 按照settings里设置的分页数进行一个分页
    page_num = request.GET.get('page', 1)  # 获取URL的页面参数(get请求)
    page_of_blogs = paginator.get_page(page_num)  # 内置的报错处理 只要是输入的不是int型 会自己默认处理成1
    currentr_page_num = page_of_blogs.number  # 获取当前页
    # 获得当前页码前后各两页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")
    # 加上首页与尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)



    # 获取博客分类对应的博客数量
    ''' 方法1
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    '''



    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates("created_time", "month", order="DESC")
    blog_dates_list = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_list[blog_date] = blog_count

    context = {}
    context["blogs"] = page_of_blogs.object_list
    context["page_of_blogs"] = page_of_blogs
    context["page_range"] = page_range
    context["blog_types"] = BlogType.objects.annotate(blog_count=Count('blog'))
    # context["blog_types"] = blog_types_list
    context["blog_dates"] = blog_dates_list
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, "blog/blog_list.html", context)


def blogs_with_type(request, blog_with_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_with_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context["blog_type"] = blog_type
    return render(request, "blog/blog_with_type.html", context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context["blogs_with_date"] = '%s年%s月' % (year, month)
    return render(request, "blog/blogs_with_date.html", context)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    # blog_content_type = ContentType.objects.get_for_model(blog)  # 获取博客类型
    # comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)  # 通过博客类型以及博客的主键值筛选得出这条博客的评论

    context = {}
    context["previous_blogs"] = Blog.objects.filter(created_time__gt=blog.created_time).last()  # 上一条博客
    context["next_blog"] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 下一条博客
    context["blog"] = blog  # 当前博客
    # context["comments"] = comments.order_by('-comment_time')  # 当前博客评论  倒序order_by('-comment_time')
    # context["comment_form"] = CommentForm(  # (reply_comment_id) 如果是顶级评论将评论ID设置为0
    #     initial={'content_type': blog_content_type, 'object_id': blog_pk,
    #              'reply_comment_id': 0})  # 实例化form里面的CommentForm方法,通过博客类型以及ID对应到博客
    # context["user"] = request.user
    context['login_form'] = LoginForms()
    response = render(request, "blog/blog_detail.html", context)
    response.set_cookie(read_cookie_key, 'true')     # 阅读标记
    return response



























































# 没有加入分页

# def blog_list(request):
#
#     page_num = request.Get.get('page',1)  #获取URL的页面参数(get请求)
#     blogs_all_list = Blog.objects.all()
#     paginat
#
#
#     context = {}
#     context["blogs"] = Blog.objects.all()
#     context["blog_types"] = BlogType.objects.all()
#     return render(request,"blog/blog_list.html", context)
#
#
#
# def blog_detail(request,blog_pk):
#     context = {}
#     context["blog"] = get_object_or_404(Blog, pk=blog_pk)
#     return render(request,"blog/blog_detail.html", context)
#
# def blogs_with_type(request,blog_with_pk):
#     context = {}
#     blog_type = get_object_or_404(BlogType,pk=blog_with_pk)
#     context["blog_type"] = blog_type
#     context["blogs"] = Blog.objects.filter(blog_type=blog_type)
#     context["blog_types"] = BlogType.objects.all()
#     return render(request,"blog/blog_with_type.html", context)
