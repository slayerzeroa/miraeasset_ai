from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from .models import *
def pb_report_list(request):
    report = {'pbreport': pbreport.objects.all()}
    return render(request, 'report_list.html', report)

def pb_report_post(request):
    if request.method == 'POST':
        contact_time = request.POST.get('contact_time')
        channel = request.POST.get('channel')
        security = request.POST.get('security')
        purpose = request.POST.get('purpose')
        content = request.POST.get('content')
        future_task = request.POST.get('future_task')

        new_report = pbreport(
            contact_time=contact_time,
            channel=channel,
            security=security,
            purpose=purpose,
            content=content,
            future_task=future_task
        )
        new_report.save()
        return HttpResponseRedirect('/pbreport/')
    else:
        return render(request, 'report_post.html')

def report_detail(request, id):
    try:
        report = pbreport.objects.get(pk=id)
    except pbreport.DoesNotExist:
        raise Http404("Does not exist!")
    return render(request, 'report_detail.html', {'report': report})