from django.urls import path
from . import views

#app_name = 'mypage'

urlpatterns = [
    path('pbpost/', views.pb_report_post, name='report_writing'),
    path('', views.pb_report_list, name='report_list'),
    path('pbpost/<int:id>', views.report_detail, name='report_detail'),
    path('pbpost/delete/<int:pk>/', views.PbreportDeleteView.as_view(), name='pbreport_delete'),
]