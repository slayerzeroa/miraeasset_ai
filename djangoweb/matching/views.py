from django.shortcuts import render
from django.http import HttpResponse
from .models import crawling
from django.template import loader
import json
from .matching_algorithm.matching import test

'''def index(request):
    news_list = crawling.objects.order_by('-date')
    template_name = loader.get_template('summary/index.html')
    context = {
        'news_list': news_list,
    }
    return HttpResponse(render(context, request))'''

def keyword(request):
    if request.method == 'POST':
        text_input = request.POST.get('text_input')
        # 여기서 text_input을 사용하여 원하는 처리를 수행합니다.
        return render(request, 'easy_news.html')
    return render(request, 'matching.html')


def service_detail(request) :
    return HttpResponse("Our service is ...")

def easy_news(request) :
    return render(request, 'easy_news.html')


def matching(request) :
    return render(request, 'matching.html')

def graph(request):
    # customer_ids = [1, 2, 3]
    # pb_ids = [101, 102]
    # connections = [(1, 101), (2, 102), (3, 101)]

    pb_ids, customer_ids, connections = test()

    context = {
        'customer_ids': json.dumps(customer_ids),
        'pb_ids': json.dumps(pb_ids),
        'connections': json.dumps(connections)
    }
    return render(request, 'graph.html', context)