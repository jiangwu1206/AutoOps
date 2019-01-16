from django.shortcuts import render
from .models import HostInfo, StatusInfo
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

# Create your views here
def index(reqeust, pIndex):
    hostlist = HostInfo.objects.all()
    p = Paginator(hostlist, 30)
    if pIndex== '':
        pIndex = '1'
    pIndex = int(pIndex)
    list = p.page(pIndex)
    plist = p.page_range
    context = {'hostlist': list, 'plist': plist, 'pIndex': pIndex}
    return render(reqeust, 'index.html', context)

def status(request, pIndex):
    a = request.GET['a']
    b = request.GET['b']
    statulist = StatusInfo.objects.filter(ip=a).filter(port=b)
    p = Paginator(statulist, 30)
    if pIndex== '':
        pIndex = '1'
    pIndex = int(pIndex)
    list = p.page(pIndex)
    plist = p.page_range
    context = {'statulist': list, 'ip': a, 'port': b, 'plist': plist, 'pIndex': pIndex}
    return render(request, 'status.html', context)

def index1(request):
    return HttpResponseRedirect("/pag?P1/")
