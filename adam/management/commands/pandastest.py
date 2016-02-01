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

def do_conversion():
    ai = AdamImport()
    ifile = ''.join([ADAM_PATH,'\Incar\Data\INVEN.DBF'])
    ofile = ''.join([ADAM_EXPORT_PATH,'INVEN.csv'])
    out_type = 'csv'

    if need_refresh(ofile):
        ai.DBFConverter(ifile,ofile,out_type)

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

ofile = ''.join([ADAM_EXPORT_PATH,'Extract.csv'])

stock = pd.read_csv(ofile)
stock.columns = ['Ford','Alternate','QOH','Days1','Days2']
stock = stock[['Alternate']].dropna()

print stock