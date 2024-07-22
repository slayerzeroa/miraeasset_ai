from django.contrib import admin
from django.urls import path, include
from config.views import home

urlpatterns = [
    path('', home),
    path('summary/', include('summary.urls')),
    path("admin/", admin.site.urls),

]
