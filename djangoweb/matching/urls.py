from django.urls import path
from .views import matching, graph, service_detail, easy_news

urlpatterns = [
    path('', matching, name='matching'),
    path('graph/', graph, name='graph'),
    path('service_detail/', service_detail, name='service_detail'),
    path('easy_news/', easy_news, name='easy_news'),
]
