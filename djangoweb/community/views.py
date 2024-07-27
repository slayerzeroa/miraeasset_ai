from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from .models import *
def community(request):
    boards = {'boards': Board.objects.all()}
    return render(request, 'report_list.html', boards)

def post(request):
    if request.method == "POST":
        author = request.POST['author']
        title = request.POST['title']
        content = request.POST['content']
        board = Board(author=author, title=title, content=content)
        board.save()
        return HttpResponseRedirect('/community/')
    else:
        return render(request, 'report_post.html')

def detail(request, id):
    try:
        board = Board.objects.get(pk=id)
    except Board.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'report_detail.html', {'board': board})