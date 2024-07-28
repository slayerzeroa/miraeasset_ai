from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import utils

'''def summary(request) :
    return render(request, 'summary.html')'''

def summary(request):
    news_data = utils.make_news_list()

    youtube_data = utils.request_url("http://ajoufe.iptime.org:5556/youtube")[:10]

    context = {
        'news_recommendations' : news_data,
        'youtube_recommendations': youtube_data
    }

    return render(request, 'summary.html', context)


def get_summary(request, news_id):
    try:
        summary_text = utils.summarize_detail(news_id)
        return JsonResponse({'summary': summary_text})
    except Exception as e:
        return JsonResponse({'summary': 'Summary not found', 'error': str(e)}, status=404)


