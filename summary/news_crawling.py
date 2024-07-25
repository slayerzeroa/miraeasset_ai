from crawling_module import *
from ClovaX_Executor import CompletionExecutor
import requests
import json

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
    url = makeUrl(keyword, start_page, end_page) # start_page = 1, end_page = 2

    #뉴스 크롤러 실행
    news_titles_ = []
    news_url_ =[]
    news_contents_ =[]
    news_dates_ = []

    if type(url) == list: # url이 list이고 원소가 2개
        for u in url:
            u_1 = articles_crawler(u)
            news_url_.append(u_1)
    else: # url이 하나
        url = articles_crawler(url)
        news_url_.append(url)
        
    #제목, 링크, 내용 담을 리스트 생성
    news_url_1 = []
    #1차원 리스트로 만들기(내용 제외)
    makeList(news_url_1,news_url_)

    #NAVER 뉴스만 남기기
    print("news_url_1 : ", news_url_1)
    final_urls = []
    for i in tqdm(range(len(news_url_1))):
        if "news.naver.com" in news_url_1[i]:
            final_urls.append(news_url_1[i])
        else:
            pass

    for i in tqdm(final_urls):
        # 각 기사 html get하기
        news = requests.get(i, headers = headers)
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
            html_date = news_html.select_one("div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
            news_date = html_date.attrs['data-date-time']
        except AttributeError:
            news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
            news_date = re.sub(pattern=pattern1,repl='',string=str(news_date))
        # 날짜 가져오기
        news_dates_.append(news_date)
    return news_titles_, final_urls, news_contents_, news_dates_

def main():
    # 키워드 검색할 요소 수집
    customer_data = request_url("http://ajoufe.iptime.org:5556/customer")[0] # 고객 데이터 불러오기
    keywords = search_keyword(customer_data)
    print(keywords)

    news_data = []
    news_titles = []
    news_url =[]
    news_contents =[]
    news_dates = []

    seen_titles = set()
    for keyword in keywords:
        news_titles, news_url, news_contents, news_dates = news_crawling(keyword)    
        for idx, i in enumerate(range(len(news_titles))):
            if news_titles[i] not in seen_titles:
                seen_titles.add(news_titles[i])
                news_data.append({
                    'id' : idx,
                    'title' : news_titles[i],
                    'url' : news_url[i],
                    'date' : news_dates[i],
                    'text' : news_contents[i],
                })
            

    news_summary_sorted = sorted(news_data, key = lambda x : x['date'], reverse = True)
    print(len(news_summary_sorted))

    with open('./news_crawling_sorted.json', 'w', encoding = 'utf-8') as f:
        json.dump(news_summary_sorted, f, ensure_ascii = False, indent = 4)
    print('Json파일로 저장되었습니다')

if __name__ == '__main__':
    main()