# miraeasset-ai

### 사용방법

#### 그래프 시각화 실행

- cd engine/matching_algorithm -> streamlit run test.py

#### Django 실행

- cd web/mysite -> python manage.py runserver

#### 뉴스 크롤링 및 요약 실행

1. 크롤링

- cd summary -> python news_crawling.py
  - 고객 데이터의 feature에서 키워드 가져와서 검색하는 방식
  - 해당 디렉토리에 news_crawling_sorted.json 파일 자동저장(날짜 순 내림차순)
  - def news_crawling(keyword) -> end_page 설정으로 뉴스 수 조절가능(보통 한 페이지당 10개 내외)

2. 요약

- cd summary -> python news_summary.py
  - 사용자가 요약 버튼 클릭하면 해당되는 id의 text를 news_crawling_sorted.json 에서 검색
  - 요약 결과 json 파일 저장 (id, summary)
  - 요약 시간 10 ~ 12초 정도 걸림

#### 유튜브 추천시스템 실행

- cd youtube_recommendation -> youtube_sorting.py
  - 해당 디렉토리에 youtube_recommend_sorted.json 파일 자동저장(유사도 순 내림차순)

#### Docker 배포

- docker build -t psyduck0/miraeasset_web:latest .
- docker push psyduck0/miraeasset_web:latest

---

### 파일구조

<!-- prettier-ignore-start -->
```
├─engine
│   ├─clustering_algorithm
│   ├─data
│   └─matching_algorithm
│   └─matching_reason
├─report_standardization
├─summary
│   ├─news_crawling
│   ├─news_summary
└─web
│   ├─mysite
│   │  ├─config
│   │  └─pybo
│   │      ├─static
│   │      │  └─public
│   │      └─templates
│   └─resource
└─youtube_recommendation
    └─youtube_sorting
```
<!-- prettier-ignore-end -->
