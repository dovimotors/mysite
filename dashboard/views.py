from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from .models import PartsInv, ServiceRO, pa_Get_Parts_Count, DailyMetrics, ARO, smooth, get_daily_service_summary
import pandas as pd
from dbftopandas import AdamImport
import datetime
from django.contrib.auth.decorators import login_required
from .forms import ServiceReports

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
    if request.method == 'POST':
        form = ServiceReports(request.POST)
        if form.is_valid():
            report = form.cleaned_data['Report']
            start_date = form.cleaned_data['StartDate']
            end_date = form.cleaned_data['EndDate']
            if report == 'ARO':
                total_gross = get_daily_service_summary('sum',form.cleaned_data['PaymentType'],False,start_date,end_date)
                total_count = get_daily_service_summary('count',form.cleaned_data['PaymentType'],False,start_date,end_date)
                data = ARO(total_gross,total_count,'DATE_OUT','ttl_sls')
                #data = smooth(aro,form.cleaned_data['Smoothing'],'ARO')
            elif report == 'Traffic':
                data = get_daily_service_summary('count',form.cleaned_data['PaymentType'],False,start_date,end_date)
                #data = smooth(data,form.cleaned_data['Smoothing'],'RO_COUNT')
            elif report == 'Gross':
                data = get_daily_service_summary('sum',form.cleaned_data['PaymentType'],False,start_date,end_date)
                #data = smooth(data,form.cleaned_data['Smoothing'],'ttl_gross')

            if data.empty:
                data = 'No Data'
            else:
                data = data.to_html(classes='pure-table', index=False)
            context = {
                'form':form,
                'data':data
            }
            return render(request, 'dashboard/service_reports.html', context)

    else:
        form = ServiceReports()
        context = {
            'form':form,
        }
    return render(request, 'dashboard/service_reports.html', context)


def parts_reports(request):
    context = {}
    return render(request, 'dashboard/parts_reports.html', context)

def parts_detail(request,start_days,end_days,field,cost=1500):
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
