from django.urls import path

from . import views

urlpatterns = [
    path('', views.keyword, name='keyword'),
    #path('<int:id>/', views.detail, name='detail'), <>는 변수를 의미하고 이 부분에 해당하는 값을 뷰에 인자로 전달
    path('easy_version/', views.easy_news, name='easy_news'),

]
#path(주소, 주소로 접근했을 때 호출할 뷰, 루트의 이름-프로젝트 메인 url과 연결해줘야 함.)