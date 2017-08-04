#coding=utf_8
from django.core.paginator import Paginator
from django.shortcuts import render
from models import TypeInfo,GoodsInfo


# Create your views here.

def index(request):
    type_list = TypeInfo.objects.all()
    list = []
    for typeinfo in type_list:
        list.append({
            'type':typeinfo,
            'list_new':typeinfo.goodsinfo_set.order_by('-id')[0:4],
            'list_click':typeinfo.goodsinfo_set.order_by('-gclick')[0:3]
        })
    context = {'title': '首页','cart':'1','list':list}
    return render(request,'tt_goods/index.html',context)


def list_goods(request,type_id,page_index):
    typeinfo = TypeInfo.objects.get(pk=type_id)

    list = typeinfo.goodsinfo_set.order_by('-id')
    list1 = typeinfo.goodsinfo_set.order_by('-id')[0:2]

    paginator = Paginator(list,10)
    page_index = int(page_index)
    if page_index <= 0:
        page_index = 1

    if page_index >= paginator.num_pages:
        page_index = paginator.num_pages

    page = paginator.page(int(page_index))

    plist = paginator.page_range
    if paginator.num_pages > 5:
        if page_index <= 2:
            plist = range(1,6)
        elif page_index >= paginator.num_pages - 1:
            plist = range(paginator.num_pages - 4, paginator.num_pages +1)
        else:
            plist = range(page_index - 2,page_index + 3)

    context = {'title': '列表页','cart': 1,'list1':list1, 'type': typeinfo, 'page': page,'pindex_list':plist}
    return render(request,'tt_goods/list.html',context)

