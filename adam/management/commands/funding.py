from django.core.management.base import BaseCommand
import sendgrid
from os import listdir
import os
import logging
from adam.models import SGFields
from mysite.settings import BASE_SHARED_PATH
from django.template.loader import render_to_string
import time

class Command(BaseCommand):

    def handle(self, *args, **options):

        def send_email(htmlbody, subject, email_list):
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

            message.add_to(email_list)
            message.set_from_name("Dovi Motors Inc.")
            message.set_from("admin@dovimotors.com")
            message.set_subject(subject)
            message.set_html(htmlbody)

            status, msg = sg.send(message)

            return (status,msg)

        #configure logger
        log_file = 'funding_log.txt'
        logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

        #assign the full path to the daily statement file
        path_to_deals = os.path.join(BASE_SHARED_PATH,'OFFICE\DEALS\\')
        flag = False
        file_list = []


        for scan_file in listdir(path_to_deals):
            if scan_file.startswith('scan'):
                logging.info('Found a scan file.  Setting flag to True.')
                flag = True
                last_modified = time.ctime(os.path.getmtime(os.path.join(path_to_deals,scan_file)))
                file_string = '%s uploaded %s ' % (scan_file,last_modified)
                file_list.append(file_string)
                context = {'file_list':file_list}
                html = render_to_string('adam\\funding.html',context)


        if flag:
            #complete the email sending tasks
            email_addresses = ["jesse@dovimotors.com", "erin@dovimotors.com", "luke@dovimotors.com"]
            s = 'There are funding docs that have not been uploaded'
            html = html
            try:
                m = send_email(html,s,email_addresses)
                logging.info(m)
            except Exception, e:
                logging.warning(m)
                logging.warning(e)

            logging.info('Sent email.  Completed funding notification process')
        else:
            logging.info('No scans found.  Aborting notification process')
