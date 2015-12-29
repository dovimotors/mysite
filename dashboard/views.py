from django.shortcuts import render, HttpResponse
from .models import PartsInv, ServiceRO
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

def parts(request):
    i = 'F:\\adamexports\\adamcache\Incar\Data\INVEN.DBF'
    o = 'output.csv'
    t = 'pandas'

    ai = AdamImport()
    inv = ai.DBFConverter(i,o,t)

    cols = ['FRANCH',
        'PARTNO',
        'SUFFIX',
        'DESC',
        'ONHAND',
        'COST',
        'EXT',
        'DATEIN',
        'DATEPURC',
        'DATESOLD']

    #only include parts that are actually in inventory
    inv = inv[inv['ONHAND'] > 0]

    #select parts that are were last purchased 45-60 days ago
    start_date = datetime.date.today() + datetime.timedelta(-60)
    end_date = datetime.date.today() + datetime.timedelta(-45)
    inv['DATEPURC'] = pd.to_datetime(inv['DATEPURC'])
    mask = (inv['DATEPURC'] < end_date) & (inv['DATEPURC'] > start_date)
    inv = inv.loc[mask]

    #add an extended cost column
    inv['EXT'] = inv['ONHAND'] * inv['COST']

    #sort by the date purchased and return an HTML table
    inv = inv.sort(['DATEPURC'])
    inv = inv[cols]
    inv = inv.to_html()
    return HttpResponse(inv)
