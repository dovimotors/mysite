from django.core.management.base import BaseCommand
import pandas as pd
from dbftopandas import AdamImport
import datetime, time
import sendgrid
import os.path
import logging
from adam.models import SGFields

class Command(BaseCommand):

    def handle(self, *args, **options):

        def send_email(htmlbody, subject):
            # using SendGrid's Python Library - https://github.com/sendgrid/sendgrid-python

            x = SGFields.objects.get(id=1)
            u = x.sgusername
            p = x.sgpassword

            sg = sendgrid.SendGridClient(u, p)
            message = sendgrid.Mail()

            """
            message.add_filter('templates', 'enable', '1')
            message.add_filter('templates', 'template_id', 'TEMPLATE-ALPHA-NUMERIC-ID')
            message.add_substitution('key', 'value')
            message.add_to("jesse@dovimotors.com")
            message.set_from("admin@dovimotors.com")
            message.set_subject("Sending with SendGrid is Fun")
            message.set_html("and easy to do anywhere, even with Python")
            message.add_to_name("Jesse Dovi")
            message.set_from_name("Dovi Motors Inc.")
            """

            message.add_to("jesse@dovimotors.com")
            message.add_to_name("Jesse Dovi")
            message.set_from_name("Dovi Motors Inc.")
            message.set_from("admin@dovimotors.com")
            message.set_subject(subject)
            message.set_html(htmlbody)

            status, msg = sg.send(message)

            return (status,msg)

        #configure logger
        log_file = 'log.txt'
        logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

        #assign the full path to the daily statement file
        daily_statement = 'DailyStatement.csv'

        #Get the last time that the DailyStatement.CSV was downloaded
        last_modified = time.ctime(os.path.getmtime(daily_statement))
        logging.info('Started floor plan notification process')
        logging.info('DailyStatement.csv files was last downloaded %s',last_modified)

        #DailyStatement.CSV should be downloaded and saved in the project folder
        try:
            fp = pd.read_table(daily_statement, sep=',', index_col=False, engine='python', header=None)
            logging.info('Successfully created the DailyStatement.csv dataframe')
        except Exception, e:
            logging.warning('There was an error creating the DailyStatement.csv dataframe')
            logging.warning(e)

        #select only records that have VEH in the 1st column
        fp = fp[(fp[0] == 'VEH')]

        #set the column names to the first line of the dataframe
        fp.columns = fp.iloc[0]

        #resest the index so that the rows are numbered in sequence
        fp = fp.reset_index(drop=True)

        #stip off the 1st line, which is a duplicate with the new columns
        fp = fp.ix[1:]

        #covert the floordate to a pandas date time field
        fp['FloorDate'] = pd.to_datetime(fp['FloorDate'])

        #select only the relevent columns
        fp = fp[['VIN','FloorDate','Interest']]

        ###########################################################
        #Begin the next section.  Ensure that adamcache has been updated before running this command

        #create the import object and set the arg variables
        ai = AdamImport()
        i = 'f:\\adamexports\\adamcache\Ficar\Data\usstock.dbf'
        o = 'output.csv'
        t = 'pandas'

        #pull in the USStock table
        try:
            temp = ai.DBFConverter(i,o,t)
            logging.info('usstock table imported successfully')
        except Exception, e:
            logging.warning('There was an error importing the usstock table')
            logging.warning(e)
            pass

        usstock = pd.read_csv('output.csv')

        #Only check the last 600 days worth of data
        cutoff_date = datetime.date.today() + datetime.timedelta(-600)
        logging.info('The usstock cutoff date is %s' % cutoff_date)


        #convert the floored date field to a date time type
        usstock['FLRDATE'] = pd.to_datetime(usstock['FLRDATE'])
        usstock = usstock[['VIN1','FLRDATE']]


        #apply the cutoff time
        usstock = usstock[usstock['FLRDATE'] > pd.to_datetime(cutoff_date)]


        #limit the rows returned
        usstock = usstock[['VIN1','FLRDATE']]


        #merge the two tables together and remove unnecessary nulls
        merged_inner = pd.merge(left=usstock,right=fp, how='right', left_on='VIN1', right_on='VIN')
        merged_inner_trunk = merged_inner[pd.isnull(merged_inner.VIN1)]
        merged_inner_trunk = merged_inner_trunk[pd.notnull(merged_inner.Interest)]

        #complete the email sending tasks
        s = 'Floored Vehicles not yet Arrived.  Last Downloaded %s' % last_modified
        html = merged_inner_trunk.to_html()
        try:
            m = send_email(html,s)
            logging.info(m)
        except Exception, e:
            logging.warning(m)
            logging.warning(e)

        logging.info('Completed floorplan notification process')

