from django.db import models
from dbftopandas import AdamImport
import pandas as pd
import numpy as np
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

def pa_Get_Parts_Count(type, start_days, end_days, field, cost=1500):
    """
    type takes either total, detail, detail_stock (this returns detail including stock parts)
    total retuns in int, sum of ONHAND
    detail return a dataframe obj with detailed records
    field can take DATEPURC or DATESOLD
    cost should be expressed as an integer in cents

    start_days should be a negative integer
    end_days should be a negative integer greater than start days
    """

    #parts needed to be in stock for DPA
    stock_file = ''.join([ADAM_EXPORT_PATH,'Extract.csv'])

    stock = pd.read_csv(stock_file)
    stock.columns = ['Ford','Alternate','QOH','Days1','Days2']
    stock = stock[['Alternate']].dropna()

    #pull the latest parts inventory from ADAM
    ai = AdamImport()
    ifile = ''.join([ADAM_PATH,'\Incar\Data\INVEN.DBF'])
    ofile = ''.join([ADAM_EXPORT_PATH,'INVEN.csv'])
    out_type = 'csv'

    #refresh the data in necessary
    if need_refresh(ofile):
        ai.DBFConverter(ifile,ofile,out_type)


    #read the CSV in a dataframe and convert the dates
    inv = pd.read_csv(ofile, engine='python')
    startdate = datetime.date.today() + datetime.timedelta(start_days)
    enddate = datetime.date.today() + datetime.timedelta(end_days)

    #initialize the parameters from the query string
    fdDate = str(field)
    #change cost to an integer and multiply by 100 to make it in dollars
    intCost = int(cost)/100

    #filter out the data
    inv = inv[inv['ONHAND']>0]
    inv = inv[inv['COST']>intCost]
    inv[fdDate] = pd.to_datetime(inv[fdDate])
    inv = inv[(inv[fdDate] < pd.to_datetime(startdate)) & (inv[fdDate] > pd.to_datetime(enddate))]
    inv['ext'] = inv['ONHAND']*inv['COST']

    #if the type is total just give a total parts value
    if type == "total":
        inv_sum = inv['ONHAND'].sum()
        return inv_sum
    #if the type is detail prepare the data for detailed export
    elif type == "detail":
        #create a full part number field to filter on
        inv['FULLPN'] = inv['PREFIX'] + inv['PARTNO'] + inv['SUFFIX']
        #create the filter to exclude stock parts
        invx = inv['FULLPN'].isin(stock['Alternate'])
        #create a new inv dataframe with out the stock parts
        inv = inv[~invx]
        inv_detail = inv[['PREFIX','PARTNO','SUFFIX','DESC','ONHAND','DATEPURC','DATESOLD','COST','ext', 'LOCATION']]
        inv_detail = inv_detail.sort(fdDate)
        return inv_detail
    elif type == "detail_stock":
        #in this case, return everything including stock parts
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

def get_daily_service_summary(type,pmttyp,body,start_date, end_date):
    """
    type currently takes sum, detail, or count
    pmttype takes C, W, I, E or 'all' for everything
    body takes true or false.  if true only return body shop ROs,
    if false returns everything buy bodyshop ROs
    """
    arrofile = ''.join([ADAM_EXPORT_PATH,'arcrof.csv'])
    rofile = ''.join([ADAM_EXPORT_PATH,'rofile.csv'])
    arcomplain = ''.join([ADAM_EXPORT_PATH,'arcomp.csv'])
    complain = ''.join([ADAM_EXPORT_PATH, 'complain.csv'])
    rof_cols = ['RO_NUM','DATE_OUT']
    comp_cols = ['RONUM','PAYMNTTYP','PAYMNTDESC','LSALES_AMT','LCOST_AMT','PSALES_AMT','PCOST_AMT','MSALES_AMT','MCOST_AMT']
    full_cols = ['RONUM','DATE_OUT','PAYMNTTYP','PAYMNTDESC','LSALES_AMT','LCOST_AMT','PSALES_AMT','PCOST_AMT','MSALES_AMT','MCOST_AMT']


    rof = pd.read_csv(rofile, usecols=rof_cols)
    rof['DATE_OUT'] = pd.to_datetime(rof['DATE_OUT'])
    rof = rof[rof['DATE_OUT']>= start_date]
    rof = rof[rof['DATE_OUT']<= end_date]


    arrof = pd.read_csv(arrofile, usecols=rof_cols)
    arrof['DATE_OUT'] = pd.to_datetime(arrof['DATE_OUT'])
    arrof = arrof[arrof['DATE_OUT']>= start_date]
    arrof = arrof[arrof['DATE_OUT']<= end_date]

    rof = rof.append(arrof)


    comp = pd.read_csv(complain, usecols=comp_cols)
    arcomp = pd.read_csv(arcomplain, usecols=comp_cols)
    if pmttyp != 'all':
        comp = comp[comp['PAYMNTTYP'].str.startswith(pmttyp, na=False)]
        arcomp = arcomp[arcomp['PAYMNTTYP'].str.startswith(pmttyp, na=False)]

    if body == True:
        comp = comp[comp['PAYMNTDESC']=='Body Shop']
        arcomp = arcomp[arcomp['PAYMNTDESC']=='Body Shop']
    else:
        comp = comp[comp['PAYMNTDESC']!='Body Shop']
        arcomp = arcomp[arcomp['PAYMNTDESC']!='Body Shop']

    comp = comp.append(arcomp)


    full_set = pd.merge(left=rof, right=comp, how='inner', left_on='RO_NUM', right_on='RONUM')
    full_set = full_set[full_cols]
    full_set['lab_gross'] = full_set['LSALES_AMT']-full_set['LCOST_AMT']
    full_set['prt_gross'] = full_set['PSALES_AMT']+full_set['MSALES_AMT']-full_set['PCOST_AMT']-full_set['MCOST_AMT']
    full_set['ttl_gross'] = full_set['prt_gross']+full_set['lab_gross']
    full_set['ttl_sls'] = full_set['LSALES_AMT']+full_set['PSALES_AMT']+full_set['MSALES_AMT']
    full_set = full_set[full_set['ttl_gross']<10000]
    full_set = full_set[full_set['ttl_gross']>-2000]


    if type=='sum':
        full_set_group = full_set.groupby(['DATE_OUT'])[['prt_gross','lab_gross','ttl_gross','ttl_sls']].agg('sum')
        full_set_group = pd.DataFrame(full_set_group).reset_index()
        return full_set_group

    elif type=='detail':
        return full_set

    elif type=='count':

        full_set_group = full_set[['DATE_OUT','RONUM']].drop_duplicates(cols='RONUM')
        full_set_group = full_set_group.groupby('DATE_OUT')[['RONUM']].size()
        full_set_group = pd.DataFrame(full_set_group).reset_index()
        full_set_group = full_set_group.rename(columns={0:'RO_COUNT'})
        return full_set_group

def ARO(df_sum,df_count,key_col,sum_col):
    """
    assumes 2 dataframes with data aggregated by day.
    key col is the column that should be used for the join
    sum_col is the name of the column that be averaged
    """
    merged = pd.merge(df_sum,df_count,how='inner', left_on=key_col, right_on=key_col)
    merged['ARO'] = merged[sum_col]/merged['RO_COUNT']
    return merged[['DATE_OUT','ARO']]

def smooth(df_data,num_deviations,col):
    """
    takes any dataframe and will drop outliers over the specified deviation from the mean.
    """
    df_data = df_data[np.abs(df_data[col]-df_data[col].mean())<=(num_deviations*df_data[col].std())]
    return df_data

def do_conversion(in_file, out_file):
    ai = AdamImport()
    ifile = ''.join([ADAM_PATH,in_file])
    ofile = ''.join([ADAM_EXPORT_PATH,out_file])
    out_type = 'csv'
    ai.DBFConverter(ifile,ofile,out_type)
    print "ran conversion %s to %s" % (in_file, out_file)