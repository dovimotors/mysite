from dbftopandas import AdamImport
import pandas as pd
import numpy as np
import datetime, time
import os
from mysite.settings import ADAM_PATH, ADAM_EXPORT_PATH


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

def do_conversion(ifile,ofile):
    ai = AdamImport()
    ifile = ''.join([ADAM_PATH,ifile])
    ofile = ''.join([ADAM_EXPORT_PATH,ofile])
    out_type = 'csv'


    #if need_refresh(ofile):
    ai.DBFConverter(ifile,ofile,out_type)
    print "conversion completed"

#do_conversion()

def check_for_parts_issue(date_to_check):
    siarctik_file = ''.join([ADAM_EXPORT_PATH,'siarctik.csv'])
    inven_file = ''.join([ADAM_EXPORT_PATH,'INVEN.csv'])
    intrack_file = ''.join([ADAM_EXPORT_PATH,'INTRACK.csv'])

    siarctik = pd.read_csv(siarctik_file)
    siarctik = siarctik[np.isfinite(siarctik['RONUM'])]
    siarctik['DATE'] = pd.to_datetime(siarctik['DATE'])
    siarctik = siarctik[siarctik['DATE'] == pd.to_datetime(date_to_check)]
    siarctik = siarctik.fillna('')
    siarctik['PN_S'] = siarctik['FRANCH'] + siarctik['PREFIX'] + siarctik['PARTNO'] + siarctik['SUFFIX']
    #siarctik = siarctik[siarctik['PN_S']=='FD9OO3113858']
    siarctik = siarctik[['RONUM','PN_S','DATE','QTY']]

    inven_raw = pd.read_csv(inven_file)
    inven = inven_raw[inven_raw['ONHAND']<10]
    inven = inven.fillna('')
    inven['PN_I'] = inven['FRANCH'] + inven['PREFIX'] + inven['PARTNO'] + inven['SUFFIX']

    inven = inven[inven['PN_I']!='FDPDMAT']
    inven = inven[['PN_I','TRACKNO']]

    intrack_raw = pd.read_csv(intrack_file)
    intrack_raw['DATE'] = pd.to_datetime(intrack_raw['DATE'])
    intrack = intrack_raw[['TRACKNO','DATE','QTY']]

    siarctik_inven_inner = pd.merge(left=siarctik,right=inven, how='inner', left_on='PN_S', right_on='PN_I')
    siarctik_inven_intrack_inner = pd.merge(left=siarctik_inven_inner,right=intrack, how='inner', left_on='TRACKNO', right_on='TRACKNO')

    siii = siarctik_inven_intrack_inner

    siii['DAYS'] = siii['DATE_x'] - siii['DATE_y']
    siii = siii[(siii['DAYS']<10)]
    siii = siii[siii['DAYS']>-10]

    #print siii

    siii = siii[['RONUM','PN_S','QTY_y']]
    siii_group = siii.groupby(['RONUM','PN_S'])[['QTY_y']].sum()
    to_check = siii_group.reset_index()


    final_filter_track = intrack_raw.dropna()
    final_filter_track = final_filter_track.groupby('TRACKNO')['TRACKNO'].count()
    final_filter_track = final_filter_track.reset_index()
    final_filter_track.columns = ['TRACKNO','COUNT']
    final_filter_track = final_filter_track[final_filter_track['COUNT']<75]
    final_filter_inven = inven_raw[inven_raw['ONHAND']>0]
    final_filter_inven['PN_I'] = final_filter_inven['FRANCH'] + final_filter_inven['PREFIX'] + final_filter_inven['PARTNO'] + final_filter_inven['SUFFIX']
    final_filter_merge1 = pd.merge(left=final_filter_track, right=final_filter_inven,how='inner',left_on='TRACKNO',right_on='TRACKNO')
    to_check = pd.merge(left=to_check, right=final_filter_merge1, how='inner', left_on='PN_S', right_on='PN_I')
    to_check = to_check[['RONUM','PN_S','QTY_y']]
    to_check = to_check[to_check['QTY_y']>0]

    return to_check

"""
dates_to_check = []

from datetime import date, timedelta as td

#Year, Month, Day, d1 = start date, d2= end date
d1 = date(2015, 03, 01)
d2 = date(2015, 06, 30)

delta = d2 - d1

for i in range(delta.days + 1):
    dates_to_check.append(str(d1 + td(days=i)))


output_file = 'c:\users\jesse\desktop\output.csv'
for dt in dates_to_check:
    x = check_for_parts_issue(dt)
    with open(output_file, 'a') as f:
        x.to_csv(f, header=False)

"""







yesterday = datetime.datetime.now().date() + datetime.timedelta(-1)

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

"""
    rof = pd.read_csv(rofile)
    rof['DATE_OUT'] = pd.to_datetime(rof['DATE_OUT'])
    rof = rof[rof_cols]
    #rof = rof[rof['STATUS']=='P']
    rof = rof[rof['DATE_OUT']>= start_date]
    rof = rof[rof['DATE_OUT']<= end_date]

    arrof = pd.read_csv(arrofile)
    arrof = arrof[rof_cols]
    arrof = arrof[arrof['DATE_OUT']>= start_date]
    arrof = arrof[arrof['DATE_OUT']<= end_date]

    rof = rof.append(arrof)


    comp = pd.read_csv(complain)
    comp = comp[comp_cols]
    arcomp = pd.read_csv(arcomplain)
    arcomp = arcomp[comp_cols]


    temp_set = pd.merge(left=rof, right=comp, how='inner', left_on='RO_NUM', right_on='RONUM')
    full_set = pd.merge(left=temp_set, right=arcomp, how='inner', left_on='RO_NUM', right_on='RONUM')
    full_set['lab_gross'] = full_set['LSALES_AMT']-full_set['LCOST_AMT']
    full_set['prt_gross'] = full_set['PSALES_AMT']-full_set['PCOST_AMT']
    full_set['ttl_gross'] = full_set['prt_gross']+full_set['lab_gross']
    full_set = full_set[full_set['ttl_gross']<10000]
    total = full_set['ttl_gross'].sum()
    full_set = full_set.groupby(['DATE_OUT'])[['prt_gross','lab_gross','ttl_gross']].sum()
    full_set = full_set.reset_index()

    return full_set
"""
"""
file_list = (('\Sicar\Data\\rofile.dbf','rofile.csv'),
             ('\Sicar\Data\\arcrof.dbf','arcrof.csv'),
             ('\Sicar\Data\\complain.dbf','complain.csv'),
             ('\Sicar\Data\\arcomp.dbf','arcomp.csv'),
         )
for x,y in file_list:
    do_conversion(x,y)
"""

startdate = '2015-02-01'
enddate = '2015-02-16'
prior_year = get_daily_service_summary('sum','all',True,startdate,enddate)
print prior_year
print prior_year['ttl_gross'].sum()


startdate = '2016-02-01'
enddate = '2016-02-16'
current_year = get_daily_service_summary('sum','all',True,startdate,enddate)

print current_year
print current_year['ttl_gross'].sum()

"""
output_file = 'c:\users\jesse\desktop\output.csv'
with open(output_file, 'w') as f:
    current_year.to_csv(f)
"""

