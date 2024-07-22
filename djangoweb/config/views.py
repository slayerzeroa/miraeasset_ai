from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    #홈화면
    return render(request, 'index.html')