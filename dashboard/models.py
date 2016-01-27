from django.db import models
from dbftopandas import AdamImport
import pandas as pd
import datetime, time
import os
from mysite.settings import ADAM_PATH, ADAM_EXPORT_PATH

# Create your models here.

#funtion to see if the file has been refreshed within 1 day
def need_refresh(file_name):
    #check to see if the file has ever been created.
    if os.path.exists(file_name):
        last_modified = str(datetime.datetime.strptime(time.ctime((os.path.getmtime(file_name))),'%a %b %d %H:%M:%S %Y'))
    else:
        #set the times if the file doesn't exists to ensure the update runs
        last_modified = datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(0,-14401)),'%Y-%m-%d %H:%M:%S')
    cut_off = datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(0,-14400)),'%Y-%m-%d %H:%M:%S')
    if last_modified < cut_off:
        return True
    else:
        return False

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

    if need_refresh(ofile):
        ai.DBFConverter(ifile,ofile,out_type)

    inv = pd.read_csv(ofile, engine='python')
    ext = inv.ONHAND * inv.COST
    ext = sum(ext)
    return ext

def pa_Get_Parts_Count(type, start_days, end_days, field, cost=15):
    """
    type takes either total or detail
    total retuns in int, sum of ONHAND
    detail return a dataframe obj with detailed records
    field can take DATEPURC or DATESOLD
    cost should be expressed as an integer

    start_days should be a negative integer
    end_days should be a negative integer greater than start days
    """

    ai = AdamImport()
    ifile = ''.join([ADAM_PATH,'\Incar\Data\INVEN.DBF'])
    ofile = ''.join([ADAM_EXPORT_PATH,'INVEN.csv'])
    out_type = 'csv'

    if need_refresh(ofile):
        ai.DBFConverter(ifile,ofile,out_type)


    inv = pd.read_csv(ofile, engine='python')
    startdate = datetime.date.today() + datetime.timedelta(start_days)
    enddate = datetime.date.today() + datetime.timedelta(end_days)

    fdDate = str(field)
    intCost = int(cost)

    inv = inv[inv['ONHAND']>0]
    inv = inv[inv['COST']>intCost]
    inv[fdDate] = pd.to_datetime(inv[fdDate])
    inv = inv[(inv[fdDate] < pd.to_datetime(startdate)) & (inv[fdDate] > pd.to_datetime(enddate))]
    inv['ext'] = inv['ONHAND']*inv['COST']

    if type == "total":
        inv_sum = inv['ONHAND'].sum()
        return inv_sum
    elif type == "detail":
        inv_detail = inv[['PREFIX','PARTNO','SUFFIX','DESC','ONHAND','DATEPURC','DATESOLD','COST','ext', 'LOCATION']]
        inv_detail = inv_detail.sort(fdDate)
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

    if need_refresh(ofile):
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