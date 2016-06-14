from django.core.management.base import BaseCommand
from mysite.settings import ADAM_PATH, ADAM_EXPORT_PATH
import pandas as pd
import numpy as np

class Command(BaseCommand):

    def handle(self, *args, **options):

        history_path = ''.join([ADAM_EXPORT_PATH,'HISTORY.csv'])
        vidfile_path = ''.join([ADAM_EXPORT_PATH,'vidfile.csv'])
        cols = ['VEHICLE','DATE','KIT','KITSUFF']
        vid_cols = ['VID','YEAR','MAKE','MODEL','VIN','DELDATE','CUSTOMER','CUSTLNAME','CUSTFNAME','ADDRESS1','ADDRESS2','CITY','STATE','ZIP','MAILER']

        history = pd.read_csv(history_path,usecols=cols)
        history['DATE'] = pd.to_datetime(history['DATE'])

        vidfile = pd.read_csv(vidfile_path,usecols=vid_cols)
        vidfile['DELDATE'] = pd.to_datetime(vidfile['DELDATE'])

        #RM101
        RM101_start_date = '2016-01-31'
        RM101_end_date = '2016-03-01'
        RM101 = history[history['DATE']> RM101_start_date]
        RM101 = RM101[RM101['DATE']< RM101_end_date]
        RM101 = RM101[RM101['KIT']=='101']
        RM101 = RM101[RM101['KITSUFF']=='RM']
        RM101['TYPE'] = 'Oil & Filter Change'
        RM101 = RM101[['VEHICLE','TYPE']]

        
        #WRKS
        WRKS_start_date = '2016-01-31'
        WRKS_end_date = '2016-03-01'
        WRKS = history[history['DATE']> WRKS_start_date]
        WRKS = WRKS[WRKS['DATE']< WRKS_end_date]
        WRKS = WRKS[WRKS['KIT']=='WRKS']
        WRKS = WRKS[WRKS['KITSUFF']=='RM']
        WRKS['TYPE'] = 'The Works'
        WRKS = WRKS[['VEHICLE','TYPE']]
        

        #101D
        RM101D_start_date = '2015-11-30'
        RM101D_end_date = '2016-01-01'
        RM101D = history[history['DATE']> RM101D_start_date]
        RM101D = RM101D[RM101D['DATE']< RM101D_end_date]
        RM101D = RM101D[RM101D['KIT']=='101D']
        RM101D = RM101D[RM101D['KITSUFF']=='RM']
        RM101D['TYPE'] = 'Diesel Oil & Filter Change'
        RM101D = RM101D[['VEHICLE','TYPE']]

        #RM103
        RM103_start_date = '2015-05-31'
        RM103_end_date = '2015-07-01'
        RM103 = history[history['DATE']> RM103_start_date]
        RM103 = RM103[RM103['DATE']< RM103_end_date]
        RM103 = RM103[RM103['KIT']=='103']
        RM103 = RM103[RM103['KITSUFF']=='RM']
        RM103['TYPE'] = 'New York State Inspection'
        RM103 = RM103[['VEHICLE','TYPE']]

        #OF Delivery Date
        OF_del_start_date = '2016-01-31'
        OF_del_end_date = '2016-03-01'
        OFDD = vidfile[vidfile['DELDATE']>OF_del_start_date]
        OFDD = OFDD[OFDD['DELDATE']<OF_del_end_date]
        OFDD['VEHICLE'] = OFDD['VID']
        OFDD['TYPE'] = 'The First Service'
        OFDD = OFDD[['VEHICLE','TYPE']]


        #NYSI Delivery Date
        NYSI_del_start_date = '2015-05-31'
        NYSI_del_end_date = '2015-07-01'
        NYSI = vidfile[vidfile['DELDATE']>NYSI_del_start_date]
        NYSI = NYSI[NYSI['DELDATE']<NYSI_del_end_date]
        NYSI['VEHICLE'] = NYSI['VID']
        NYSI['TYPE'] = 'New York State Inspection'
        NYSI = NYSI[['VEHICLE','TYPE']]

        #Combine resulting dataframes and get address info
        exclusion_list_lname = ['PURGE','DOVI MOTORS INC']
        exclusion_list_city = ['MOVED']
        inclusion_list_state = ['NY','PA','NJ','MA','VT','OH']
        combined = RM101.append(WRKS)
        combined = combined.append(RM101D)
        combined = combined.append(OFDD)
        combined = combined.append(NYSI)
        combined = combined.append(RM103)

        all_data = pd.merge(combined,vidfile,how='inner',left_on='VEHICLE',right_on='VID')

        #removed unwanted records from the combined and merged data
        all_data = all_data[all_data['MAILER']=='Y']
        all_data = all_data[~all_data['CUSTLNAME'].isin(exclusion_list_lname)]
        all_data = all_data[~all_data['CITY'].isin(exclusion_list_city)]
        all_data = all_data[all_data['STATE'].isin(inclusion_list_state)]

        #sortby ZIP and export
        cols_to_export = ['YEAR','MAKE','MODEL','CUSTLNAME','CUSTFNAME','ADDRESS1','ADDRESS2','CITY','STATE','ZIP','TYPE']
        all_data = all_data[cols_to_export]
        all_data = all_data.sort(columns='ZIP')
        output = 'C:\Users\jesse\Desktop\output.csv'
        #all_data.to_csv(output,index=False)
        g = all_data.groupby(np.arange(len(all_data)) // 8).apply(lambda x: x.reset_index(0, drop=True))
        suffix = 0

        final_df = g.iloc[(g.index.get_level_values(0)==0)]

        #print (g)

        #for df in g.groups:
            #final_df = pd.merge(final_df,df,left_on=final_df.index.get_level_values(1),right_on=df.index.get_level_values(1),suffixes=('',suffix))
        #    print (df)
        output = 'C:\Users\jesse\Desktop\output.csv'
        g.to_csv(output)
        """
        df1 = g.iloc[(g.index.get_level_values(0)==0)]
        df2 = g.iloc[(g.index.get_level_values(0)==1)]
        final_df = pd.merge(df1,df2,left_on=df1.index.get_level_values(1),right_on=df2.index.get_level_values(1),suffixes=('','2'))
        print (final_df)
        """

        """
        #Testing against data pull from ADAM
        all_data = all_data[all_data['TYPE']=='New York State Inspection']

        f = 'f:\winADAM\Mdcar\Mail List\June2016NYSI.dat'
        adam_of = pd.read_table(f, sep=',', index_col=False, engine='python', header=None)
        #print adam_of
        merged = pd.merge(all_data,adam_of,how='left',left_on='VIN',right_on=10)

        merged = merged[merged[10].isnull()]
        print merged[['VIN',10,'CUSTLNAME']]
        #output = 'C:\Users\jesse\Desktop\output.csv'
        #merged.to_csv(output)
        """



