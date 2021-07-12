import datetime
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, ReadDetail
from django.utils import timezone


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):   #判断当前访问cookies 是否存在
        #当前阅读数量加一
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)  #比下面的方法更简单  (不存在就创建)
        readnum.read_num += 1
        readnum.save()


        #当天阅读数加一
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)  #如果当前时间的这条博客没有访问记录,就直接创建一条
        readDetail.read_num += 1
        readDetail.save()
    return key

"""
      # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     # 存在记录     (这里的记录是指没有阅读记录,见笔记)
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     # 不存在记录
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)
        #     # a = 1
        # readnum.read_num += 1
        # readnum.save()
        # date = timezone.now().date()      #获取当前时间(准确的说是数据库的时间)
        # if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():  #这里判断数据库中是不是有这个时间这条博客的访问记录
        #     readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)  #把当前时间,当前ID的博客的阅读记录取出来
        # else:
        #     readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)     #如果当前时间的这条博客没有记录,就直接创建一条
        # readDetail.read_num += 1
        # readDetail.save()
    # return key
"""

def get_seven_days_read_date(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(6, -1, -1):  #获取七天的差值
        date = today - datetime.timedelta(days=i)  #这里用今天的时间减去一天时间,就是昨天这个时间
        dates.append(date.strftime("%m/%d"))  #按照年月的形式存入时间集合
        read_detils = ReadDetail.objects.filter(content_type=content_type, date=date)  #查询七天的博客阅读量
        result = read_detils.aggregate(read_num_sum=Sum("read_num"))   #使用聚合函数aggregate  #把每一篇的博客阅读量加在一起
        read_nums.append(result["read_num_sum"] or 0)    #(result["read_num_sum"] or 0)做逻辑判断  如果前面是空的就取0 如果不是空的就正常取值
    return dates, read_nums

def get_today_hot_data(content_type):
    today = timezone.now().date()      #获取今天的时间
    read_detils = ReadDetail.objects.filter(content_type=content_type, date=today).order_by("-read_num")  # 查询今天的博客阅读量  然后筛选排序
    return read_detils[:7]

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()      #获取今天的时间
    yesterday = today - datetime.timedelta(days=1)  #获取一天前的时间
    read_detils = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by("-read_num")  # 查昨天的博客阅读量  然后筛选排序(-read_num  倒序)
    return read_detils[:7]


def get_hebdomad_hot_data(content_type):

    today = timezone.now().date()      #获取今天的时间
    hebdomad = today - datetime.timedelta(days=7)
    read_detils = ReadDetail.objects\
        .filter(content_type=content_type, date__lt=today, date__gte=hebdomad)\
        .annotate(read_num_sum=Sum("read_num"))\
        .order_by("-read_num_sum")  # 查询七天的博客阅读量  然后筛选排序
    return read_detils[:5]