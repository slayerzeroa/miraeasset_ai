from django.urls import path
from . import views

#app_name = 'mypage'

urlpatterns = [
    path('post/', views.pb_report_post, name='report_writing'),
    path('', views.pb_report_list, name='report_list'),
    path('post/<int:id>', views.report_detail, name='report_detail'),
]