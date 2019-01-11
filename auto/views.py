from django.shortcuts import render
from .models import HostInfo, StatusInfo
from django.core.paginator import Paginator

# Create your views here
def index(reqeust):
    hostlist = HostInfo.objects.all()
    context = {'hostlist': hostlist}
    return render(reqeust, 'index.html', context)

def status(request, ip, ip1, ip2, ip3):
    statulist = StatusInfo.objects.all()
    context = {'statulist': statulist, 'ip': ip}
    return render(request, 'status.html', context)

