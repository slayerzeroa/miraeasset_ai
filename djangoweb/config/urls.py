from django.contrib import admin
from django.urls import path, include
from config.views import home

urlpatterns = [
    path('', home, name='main'),
    path('main/', home),
    path('summary/', include('summary.urls'), name='summary'),
    path("admin/", admin.site.urls, name='admin'),
    path("matching/", include("matching.urls"), name='matching'),
]
