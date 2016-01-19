from django.shortcuts import render, HttpResponse
from .models import PartsInv, ServiceRO, pa_Get_Parts_Count, DailyMetrics
import pandas as pd
from dbftopandas import AdamImport
import datetime
# Create your views here.


def index(request):
    parts = PartsInv.objects.all()
    service = ServiceRO.objects.all()
    context = {'parts_list': parts,
               'service_list':service,
               }
    return render(request, 'dashboard/index.html', context)

def service(request):
    ro_data = pd.DataFrame(list(ServiceRO.objects.all().values()))
    html = ro_data.to_html()
    return HttpResponse(html)

def parts_detail(request,start_days,end_days):
    invert_start = int(start_days)*-1
    invert_end = int(end_days)*-1
    inv = pa_Get_Parts_Count('detail',invert_start,invert_end)
    html = inv.to_html()
    return HttpResponse(html)

def all_metrics(request):
    metrics = DailyMetrics.objects.all()
    context = {'daily_metrics': metrics}
    return render(request, 'dashboard/all_metric_data.html',context)
