from django.shortcuts import render, HttpResponse, render_to_response
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
    #branch for GET vs. POST
    if request.method == 'POST':
        form = ServiceReports(request.POST)
        if form.is_valid():
            #extract the variables from the POST data
            report = form.cleaned_data['Report']
            start_date = form.cleaned_data['StartDate']
            end_date = form.cleaned_data['EndDate']
            body_shop = form.cleaned_data['BodyShop']
            export = form.cleaned_data['Export']
            if report == 'ARO':
                total_gross = get_daily_service_summary('sum',form.cleaned_data['PaymentType'],body_shop,start_date,end_date)
                total_count = get_daily_service_summary('count',form.cleaned_data['PaymentType'],body_shop,start_date,end_date)
                data = ARO(total_gross,total_count,'DATE_OUT','ttl_sls')
                data = smooth(data,form.cleaned_data['Smoothing'],'ARO')
            elif report == 'Traffic':
                data = get_daily_service_summary('count',form.cleaned_data['PaymentType'],body_shop,start_date,end_date)
                data = smooth(data,form.cleaned_data['Smoothing'],'RO_COUNT')
            elif report == 'Gross':
                data = get_daily_service_summary('sum',form.cleaned_data['PaymentType'],body_shop,start_date,end_date)
                data = smooth(data,form.cleaned_data['Smoothing'],'ttl_gross')

            #if an empty dataframe is returned show "no data"
            if data.empty:
                data = 'No Data'
            else:
                html_data = data.to_html(classes='pure-table', index=False, float_format=lambda x: '%10.2f' % x)
            context = {
                'form':form,
                'data':html_data
            }

            #If export is checked read the dataframe to a stringIO object
            if export:
                import StringIO
                buf = StringIO.StringIO()

                #read the dataframe to the IO buffer, then store the results in a variable.
                data.to_csv(buf)
                datafile = buf.getvalue()

                # generate the response
                response = HttpResponse(datafile, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=%s.csv' % report
                return response
            else:
                return render(request, 'dashboard/service_reports.html', context)

        #If the form data isn't valid, return an error
        else:
            context = {
                'form': form,
                'data': 'There was a problem with the form data'
            }
            return render(request, 'dashboard/service_reports.html', context)

    #if there is no post data then show the blank form
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
    metrics = DailyMetrics.objects.all().order_by('-id')[:45]
    context = {'daily_metrics': metrics}
    return render(request, 'dashboard/all_metric_data.html',context)
