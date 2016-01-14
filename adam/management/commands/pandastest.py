from dbftopandas import AdamImport
import pandas as pd
import datetime, time
import os

ai = AdamImport()
ifile = 'F:\\adamexports\\adamcache\Incar\Data\INVEN.DBF'
ofile = 'F:\\adamexports\csvfiles\INVEN.csv'
out_type = 'csv'

ai.DBFConverter(ifile,ofile,out_type)


inv = pd.read_csv(ofile, engine='python')
startdate = datetime.date.today() + datetime.timedelta(-29)
enddate = datetime.date.today() + datetime.timedelta(-45)

inv = inv[inv['ONHAND']>0]
inv = inv[inv['COST']>15]
inv['DATEPURC'] = pd.to_datetime(inv['DATEPURC'])
inv = inv[(inv['DATEPURC'] < pd.to_datetime(startdate)) & (inv['DATEPURC'] > pd.to_datetime(enddate))]
count = inv['ONHAND'].sum()
inv['ext'] = inv['ONHAND']*inv['COST']

inv_detail = inv[['PREFIX','PARTNO','SUFFIX','DESC','ONHAND','DATEPURC','DATESOLD','COST','ext', 'LOCATION']]
inv_sum = inv['ONHAND'].sum()

print inv_detail, inv_sum