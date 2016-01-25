from dbftopandas import AdamImport
import pandas as pd
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

ai = AdamImport()
ifile = ''.join([ADAM_PATH,'\Incar\Data\INVEN.DBF'])
ofile = ''.join([ADAM_EXPORT_PATH,'INVEN.csv'])
out_type = 'csv'

"""
last_modified = datetime.datetime.strptime(time.ctime((os.path.getmtime(ofile))),'%a %b %d %H:%M:%S %Y')
cut_off = datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(0,-14400)),'%Y-%m-%d %H:%M:%S')

print last_modified
print cut_off
"""
if need_refresh(ofile):
    print "do the update"
else:
    print "dont do the update"
#ai.DBFConverter(ifile,ofile,out_type)