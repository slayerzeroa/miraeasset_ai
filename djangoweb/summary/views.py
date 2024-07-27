from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from . import utils


def keyword(request):
    if request.method == 'POST':
        text_input = request.POST.get('text_input')
        # 여기서 text_input을 사용하여 원하는 처리를 수행합니다.
        return render(request, 'easy_news.html')
    return render(request, 'keyword.html')


def summary(request):
    return render(request, 'summary.html', {
        'articles': {"title": "[🙋마이턴] EP.3 내 자식의 성공은 곧 나의 성공! VS내 노후는 아무도 책임져주지 않아! l 2022.11.09(수)",
                     "content": "이 영상에서는 \"내 자식의 성공은 곧 나의 성공! VS 내 노후는 아무도 책임져주지 않아!\"라는 주제로 자녀 주식 투자와 나의 노후 준비에 대해 토론합니다. 나루맘 박수진 연구위원과 2남2녀 김석환 선임연구위원이 서로 다른 스타일로 치열한 토론을 펼치며, 시청자들은 자신이 공감하는 의견에 투표하고 응원 댓글을 작성할 수 있습니다. 이를 통해 금융과 경제에 대한 다각적인 시각을 얻을 수 있으며, 자신의 노후 준비와 자녀 주식 투자에 대한 고민을 함께 나눌 수 있습니다.",
                     "similarity": 0.9450771809,
                     "url": "https:\/\/www.youtube.com\/watch?v=OCi3PgmBsJw&list=PL1-YXgQy7nWxtpKbHMPjhD_nSNcWE5d8U&index=3"}})


def test(request):
    return render(request, 'summary.html', {
        'articles': {"title": "[🙋마이턴] EP.3 내 자식의 성공은 곧 나의 성공! VS내 노후는 아무도 책임져주지 않아! l 2022.11.09(수)",
                     "content": "이 영상에서는 \"내 자식의 성공은 곧 나의 성공! VS 내 노후는 아무도 책임져주지 않아!\"라는 주제로 자녀 주식 투자와 나의 노후 준비에 대해 토론합니다. 나루맘 박수진 연구위원과 2남2녀 김석환 선임연구위원이 서로 다른 스타일로 치열한 토론을 펼치며, 시청자들은 자신이 공감하는 의견에 투표하고 응원 댓글을 작성할 수 있습니다. 이를 통해 금융과 경제에 대한 다각적인 시각을 얻을 수 있으며, 자신의 노후 준비와 자녀 주식 투자에 대한 고민을 함께 나눌 수 있습니다.",
                     "similarity": 0.9450771809,
                     "url": "https:\/\/www.youtube.com\/watch?v=OCi3PgmBsJw&list=PL1-YXgQy7nWxtpKbHMPjhD_nSNcWE5d8U&index=3"}})


def summary_easy_version(request):
    utils.crawling()
    json_file_path = 'summary/static/summary/news_crawling_sorted.json'

    # JSON 파일 읽기
    with open(json_file_path, 'r', encoding='utf-8') as file:
        news_data = json.load(file)

    return render(request, 'easy_news.html', {'news_data': news_data})


def get_summary(request, post_id):
    try:
        summary_text = utils.summarize_detail(post_id)
        return JsonResponse({'summary': summary_text})
    except Exception as e:
        return JsonResponse({'summary': 'Summary not found', 'error': str(e)}, status=404)

