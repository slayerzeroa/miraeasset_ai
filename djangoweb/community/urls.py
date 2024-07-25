from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post, name='writing'),
    path('', views.community, name='community'),
    path('post/<int:id>', views.detail, name='detail'),
]