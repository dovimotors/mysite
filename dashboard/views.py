from django.shortcuts import render, HttpResponse
from .models import PartsInv, ServiceRO, pa_Get_Parts_Count
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

def parts_detail(request):
    inv = pa_Get_Parts_Count('detail',-29,-45)
    inv.to_html
    return HttpResponse(inv)
