import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

import re
from tqdm import tqdm

# 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
  #입력된 수를 1, 11, 21, 31 ...만들어 주는 함수
def makePgNum(num):
    if num == 1:
        return num
    elif num == 0:
        return num+1
    else:
        return num+9*(num-1)

# 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)

def makeUrl(search, start_pg, end_pg):
    if start_pg == end_pg:
        start_page = makePgNum(start_pg)
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(start_page)
        print("생성url: ", url)
        return url
    else:
        urls = []
        for i in range(start_pg, end_pg + 1):
            page = makePgNum(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page)
            urls.append(url)
        print("생성url: ", urls)
        return urls

# html에서 원하는 속성 추출하는 함수 만들기 (기사, 추출하려는 속성값)
def news_attrs_crawler(articles,attrs):
    attrs_content=[]
    for i in articles:
        attrs_content.append(i.attrs[attrs])
    return attrs_content

# ConnectionError방지
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

#html생성해서 기사크롤링하는 함수 만들기(url): 링크를 반환
def articles_crawler(url):
    #html 불러오기
    original_html = requests.get(url,headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")

    url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
    url = news_attrs_crawler(url_naver,'href')
    return url

#제목, 링크, 내용 1차원 리스트로 꺼내는 함수 생성
def makeList(newlist, content):
    for i in content:
        for j in i:
            newlist.append(j)
    return newlist

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        full_response = ""
        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data:"):
                        json_data = decoded_line[5:].strip()  # 'data:' 이후의 내용 추출 및 공백 제거
                        try:
                            response_json = json.loads(json_data)
                            if "message" in response_json and "content" in response_json["message"] and response_json["outputLength"] != 1:
                                full_response += response_json["message"]["content"]
                        except json.JSONDecodeError:
                            print("Error: Failed to decode JSON")
        self.full_response = full_response


def request_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Fail to retrieve data. Status code : {response.status_code}")


def search_keyword(customer_data):
    customer_interests = [customer_data['Preferred_Investment_Types'], customer_data['Preferred_Investment_Topics']]
    keywords = []
    for interest in customer_interests:
        keywords.append(interest)
    return keywords


def news_crawling(keyword):
    # naver url 생성
    start_page = 1
    end_page = 2
    url = makeUrl(keyword, start_page, end_page)  # start_page = 1, end_page = 2

    # 뉴스 크롤러 실행
    news_titles_ = []
    news_url_ = []
    news_contents_ = []
    news_dates_ = []

    if type(url) == list:  # url이 list이고 원소가 2개
        for u in url:
            u_1 = articles_crawler(u)
            news_url_.append(u_1)
    else:  # url이 하나
        url = articles_crawler(url)
        news_url_.append(url)

    # 제목, 링크, 내용 담을 리스트 생성
    news_url_1 = []
    # 1차원 리스트로 만들기(내용 제외)
    makeList(news_url_1, news_url_)

    # NAVER 뉴스만 남기기
    print("news_url_1 : ", news_url_1)
    final_urls = []
    for i in tqdm(range(len(news_url_1))):
        if "news.naver.com" in news_url_1[i]:
            final_urls.append(news_url_1[i])
        else:
            pass

    for i in tqdm(final_urls):
        # 각 기사 html get하기
        news = requests.get(i, headers=headers)
        news_html = BeautifulSoup(news.text, "html.parser")

        # 뉴스 제목 가져오기
        title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
        if title == None:
            title = news_html.select_one("#content > div.end_ct > div > h2")

        # 뉴스 본문 가져오기
        content = news_html.select("article#dic_area")
        if content == []:
            content = news_html.select("#articeBody")

        content = ''.join(str(content))

        # html태그제거 및 텍스트 다듬기
        pattern1 = '<[^>]*>'
        title = re.sub(pattern=pattern1, repl='', string=str(title))
        content = re.sub(pattern=pattern1, repl='', string=content)
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        content = content.replace(pattern2, '')

        news_titles_.append(title)
        news_contents_.append(content)

        try:
            html_date = news_html.select_one(
                "div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
            news_date = html_date.attrs['data-date-time']
        except AttributeError:
            news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
            news_date = re.sub(pattern=pattern1, repl='', string=str(news_date))
        # 날짜 가져오기
        news_dates_.append(news_date)
    return news_titles_, final_urls, news_contents_, news_dates_


def crawling():
    # 키워드 검색할 요소 수집
    customer_data = request_url("http://ajoufe.iptime.org:5556/customer")[0]  # 고객 데이터 불러오기
    keywords = search_keyword(customer_data)
    print(keywords)

    news_data = []

    seen_titles = set()
    for keyword in keywords:
        news_titles, news_url, news_contents, news_dates = news_crawling(keyword)
        for idx, i in enumerate(range(len(news_titles))):
            if news_titles[i] not in seen_titles:
                seen_titles.add(news_titles[i])
                news_data.append({
                    'id': idx,
                    'title': news_titles[i],
                    'url': news_url[i],
                    'date': news_dates[i],
                    'text': news_contents[i],
                })

    news_summary_sorted = sorted(news_data, key=lambda x: x['date'], reverse=True)

    # 파일을 summary/static 폴더에 저장
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    summary_static_dir = os.path.join(static_dir, 'summary')
    if not os.path.exists(summary_static_dir):
        os.makedirs(summary_static_dir)
    file_path = os.path.join(summary_static_dir, 'news_crawling_sorted.json')

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(news_summary_sorted, f, ensure_ascii=False, indent=4)

def summarize_detail(id):
    # api
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY63IHRsuPbkmleZBGwzFCDyaHMUZtTU7D+D0PfCHfrjO',
        api_key_primary_val='2OJqSbHoUuBfEh0oRCoPrCDXRgT5TTElucAkTiXK',
        request_id='bd80a896-87c9-444e-8c71-de12be1d314d'
    )

    # json파일에서 클릭된 뉴스의 id를 조회 -> 해당 id에 속하는 뉴스 text 가져오기
    json_path = 'summary/static/summary/news_crawling_sorted.json'
    #id = 11
    news_crawling_json = pd.read_json(json_path, orient="records")
    news_text = news_crawling_json[news_crawling_json['id'] == id]['text'].values[0]

    # 요약 버튼 클릭하면 news_text에 입력되도록
    preset_text = [
        {"role":"system","content":"<명령문>\n당신은 뉴스 요약 어시스턴트입니다. 당신의 요약을 보는 고객은 금융 투자를 하고있는 만 65세 이상 고령층입니다. 고령층 고객들이 뉴스 기사를 보기 쉽게 핵심 내용을 추출하여 요약해야 합니다.\n예시와 지침을 참고하여 작업을 진행하세요.\n\n\n<예시>\n### 뉴스\n\"달러당 1300원까지는 '아직은 감내할 수 있을 정도'라는 안정감이 있다. 하지만 1400원이 넘어가면 원화값 방어가 가능할지에 대한 시장의 불안감이 급증한다.\" 외환당국의 한 고위 관계자는 16일 매일경제와 통화하며 이 같은 고민을 내비쳤다. 이날 오후 최상목 대통령실 경제수석은 대통령실 브리핑을 통해 \"한국과 미국 정상 간 포괄적 외환시장 안정화 협력에 대한 추가 논의가 있을 것\"이라고 언급했다. 그의 발언 직후 원화값은 수직 상승해 전일 종가 대비 5.7원 오른 달러당 1388.0원에 마무리했다. 원화값은 전일 1393.7원까지 떨어져 1400원 선 붕괴를 눈앞에 뒀었다.\n\n\n최 수석은 다음주 뉴욕에서 만나는 윤석열 대통령과 조 바이든 미국 대통령 간 통화스왑 논의가 있을 것인지 묻는 질문에 \"어떤 게 논의될지 정상들 간 만나보셔야 알 수 있는 상황이다. 양국 정상이 지난 5월 정상회담에서 외환시장에 대해 긴밀히 협의하기로 했고, 뉴욕에서 재무장관 회담도 예정된 만큼 이와 관련된 공통 관심사를 자연스럽게 논의할 것으로 예상한다\"고 원론적으로 말했다. 일단 외환당국은 통화스왑을 실질적으로 추진해야 할 상황은 아니라는 기류가 강하다. 지금은 주요 통화에 비해 달러 강세가 뚜렷할 뿐 한국의 달러 조달 역량이 위협받고 있지 않다는 이유에서다. 실제로 대표적 국가 신인도 지표인 한국 국채에 대한 신용부도스왑(CDS) 프리미엄은 15일 32bp로 전일 대비 변화가 없었고 아직 코로나19 사태 초기 수준인 50bp를 밑돌고 있다. 한 기획재정부 관계자는 \"한미 통화스왑 체결이 외환시장에 긍정적 요인이 될 수 있을 것이라는 점에는 공감한다\"면서도 \"현재 외화 유동성 등을 살펴봤을 때 통화스왑 체결이 당장 필요한 상황은 아닌 것으로 판단된다\"고 말했다.\n\n### 결과\n요약문 : 한국 원-달러 환율이 1400원에 가까워지면서 시장의 불안감이 커지고 있습니다. 최상목 경제수석은 한국과 미국 정상 간 외환시장 안정화 협력에 대한 논의가 있을 것이라고 밝혔습니다. 그의 발언 이후 원화 가치는 상승해 달러당 1388.0원으로 마감되었습니다. 외환당국은 현재 통화스왑 추진이 필요하지 않다고 보고 있으며, 한국의 달러 조달 능력이 안정적이라고 설명했습니다. 한국 국채 신용부도스왑(CDS) 프리미엄도 안정적인 수준을 유지하고 있습니다.\r\n\r\n금융 용어 :\r\n- 환율: 두 나라의 화폐 교환 비율을 말합니다. 예를 들어, 원-달러 환율이 1300원이라면 1달러를 사기 위해 1300원이 필요합니다.\r\n- 외환시장 안정화 협력: 국가 간 화폐 가치의 급격한 변동을 막기 위해 협력하는 것을 의미합니다.\r\n- 통화스왑: 두 나라가 서로의 통화를 일정 기간 교환하기로 약속하는 금융 계약입니다. 이를 통해 외환시장에 유동성을 공급할 수 있습니다.\r\n- 신용부도스왑(CDS) 프리미엄: 국가나 기업이 부도날 위험을 대비해 보험료처럼 지불하는 비용입니다. 이 프리미엄이 낮을수록 신용도가 높다는 의미입니다.\n\n\n\n<지침>\n아래 지침을 준수하여 주어진 뉴스를 분석하고 500자 내외로 요약하세요. 추가적으로 고령층이 어려워할 수 있는 금융 용어에 대해서는 따로 용어 정리를 진행해주세요.\n\r\n1. 주어진 텍스트의 전체적인 맥락과 주제를 파악합니다.\r\n2. 불필요한 세부사항은 제외하고 간결하고 명확한 문장으로 요약을 작성해야 하며, 문장간 연결성이 유지되는지 확인하세요.\r\n3. 요약문은 만 65세 이상 고령층에 전해집니다. 고령층은 뉴스기사의 내용을 어려워하는 경우가 있습니다. 쉽게 풀어서 작성해주세요.\r\n4. 용어 정리에 들어가는 용어는 반드시 요약문에도 포함이 되어 있어야 합니다.\r\n5. 위의 지침을 철저히 따라 고품질의 텍스트 요약을 제공합니다.\n\n\n<출력>\n### 요약문 :\n### 용어 정리 : "},
        {"role": "user", "content": f"다음 뉴스를 요약하고, 어려운 금융 용어를 설명하세요.\n\n# 뉴스 : {news_text}"}
    ]

    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 512,
        'temperature': 0.08,
        'repeatPenalty': 1.2,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }
    completion_executor.execute(request_data)
    summary = completion_executor.full_response

    return summary