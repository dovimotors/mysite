from django.db import models
from dbftopandas import AdamImport
import pandas as pd
import datetime, time
import os

# Create your models here.


class PartsInv(models.Model):

    #def __str__(self):
    #   return self.statdate

    statdate = models.DateField(auto_now=True)
    invvalue = models.FloatField()

class ServiceRO(models.Model):

    statdate = models.DateField(auto_now=True)
    totalrocount = models.IntegerField()
    oldrocount = models.IntegerField()
    printedrocount = models.IntegerField()
    ro_custpay = models.FloatField()
    ro_intpay = models.FloatField()
    ro_warpay = models.FloatField()
    ro_extpay = models.FloatField()

class DailyMetrics(models.Model):
    """
    field prefixes use the following codes
    pa - parts
    sv - service
    sa - sales
    ac - accounting
    """
    statdate = models.DateField(auto_now=True)

    #parts metrics
    pa_invvalue = models.FloatField(null=True, blank=True, max_length=100)
    pa_count30to45 = models.IntegerField(null=True, blank=True)
    pa_count60to65 = models.IntegerField(null=True, blank=True)

    #service metrics
    sv_ro_count = models.IntegerField(null=True, blank=True)
    sv_old_ro_count = models.IntegerField(null=True, blank=True)

#parts functions
def pa_Get_Inventory_Value():
    ai = AdamImport()
    ifile = 'F:\\adamexports\\adamcache\Incar\Data\INVEN.DBF'
    ofile = 'F:\\adamexports\csvfiles\INVEN.csv'
    out_type = 'csv'

    ai.DBFConverter(ifile,ofile,out_type)

    inv = pd.read_csv(ofile, engine='python')
    ext = inv.ONHAND * inv.COST
    ext = sum(ext)
    return ext

def pa_Get_Parts_Count(type, start_days, end_days):
    """
    type takes either total or detail
    total retuns in int, sum of ONHAND
    detail return a dataframe obj with detailed records

    start_days should be a negative integer
    end_days should be a negative integer greater than start days
    """

    ai = AdamImport()
    ifile = 'F:\\adamexports\\adamcache\Incar\Data\INVEN.DBF'
    ofile = 'F:\\adamexports\csvfiles\INVEN.csv'
    out_type = 'csv'

    ai.DBFConverter(ifile,ofile,out_type)


    inv = pd.read_csv(ofile, engine='python')
    startdate = datetime.date.today() + datetime.timedelta(start_days)
    enddate = datetime.date.today() + datetime.timedelta(end_days)

    inv = inv[inv['ONHAND']>0]
    inv = inv[inv['COST']>15]
    inv['DATEPURC'] = pd.to_datetime(inv['DATEPURC'])
    inv = inv[(inv['DATEPURC'] < pd.to_datetime(startdate)) & (inv['DATEPURC'] > pd.to_datetime(enddate))]
    inv['ext'] = inv['ONHAND']*inv['COST']

    if type == "total":
        inv_sum = inv['ONHAND'].sum()
        return inv_sum
    elif type == "detail":
        inv_detail = inv[['PREFIX','PARTNO','SUFFIX','DESC','ONHAND','DATEPURC','DATESOLD','COST','ext', 'LOCATION']]
        return inv_detail



#service functions
def sv_Get_RO_Count(type):
    """

    type:valid options are totalcount, oldcount

    """
    ai = AdamImport()

    ifile = 'F:\\adamexports\\adamcache\Sicar\Data\\rofile.dbf'
    ofile = 'F:\\adamexports\csvfiles\\rofile.csv'
    out_type = 'csv'

    ai.DBFConverter(ifile,ofile,out_type)

    rof = pd.read_csv(ofile, engine='python')
    cutoff_date = datetime.date.today() + datetime.timedelta(-30)

    ttlcount = rof.RO_NUM.count()
    rof['DATE_IN'] = pd.to_datetime(rof['DATE_IN'])
    oldcount = rof[rof['DATE_IN'] < pd.to_datetime(cutoff_date)]
    oldcount = oldcount['RO_NUM'].count()
    if type == 'totalcount':
        return ttlcount
    elif type == 'oldcount':
        return oldcount