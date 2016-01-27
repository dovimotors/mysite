from django.shortcuts import render, HttpResponse
from .models import PartsInv, ServiceRO, pa_Get_Parts_Count, DailyMetrics
import pandas as pd
from dbftopandas import AdamImport
import datetime
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    parts = PartsInv.objects.all()
    service = ServiceRO.objects.all()
    context = {'parts_list': parts,
               'service_list':service,
               }
    return render(request, 'dashboard/index.html', context)

@login_required
def service(request):
    ro_data = pd.DataFrame(list(ServiceRO.objects.all().values()))
    html = ro_data.to_html()
    return HttpResponse(html)

def parts_reports(request):
    context = {}
    return render(request, 'dashboard/parts_reports.html', context)

def parts_detail(request,start_days,end_days,field,cost=15):
    invert_start = int(start_days)*-1
    invert_end = int(end_days)*-1
    inv = pa_Get_Parts_Count('detail',invert_start,invert_end,field,cost)
    html = inv.to_html()
    return HttpResponse(html)

@login_required
def all_metrics(request):
    metrics = DailyMetrics.objects.all()[:45]
    context = {'daily_metrics': metrics}
    return render(request, 'dashboard/all_metric_data.html',context)
