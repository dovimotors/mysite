from django.core.management.base import BaseCommand
import sendgrid
from dashboard.models import pa_Get_Parts_Count, get_service_parts_detail
from adam.models import SGFields
from django.template.loader import render_to_string
import datetime, time
import os
from mysite.settings import ADAM_PATH, ADAM_EXPORT_PATH

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('email_type')

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


        email_type = options['email_type']

        if email_type == "parts_30to45":
            part_list =  pa_Get_Parts_Count('detail',-29,-45,'DATEPURC')

            html = part_list.to_html()
            subject = "Parts 30 to 45 days old"
            email_addresses = ["jesse@dovimotors.com","gordy@dovimotors.com","robin@dovimotors.com"]
            send_email(html,subject,email_addresses)

        elif email_type == "parts_monthly":
            file_path = ''.join([ADAM_EXPORT_PATH,'Extract.csv'])
            last_modified = time.ctime(os.path.getmtime(file_path))
            modified_message = 'The stock parts file was last updated %s' % last_modified
            context = {
                'headline':'Monthly Aged Parts Reports',
                'body':'This is a reminder to run the monthly aged parts inventory reports.',
                'last_modified': last_modified
            }
            html = render_to_string('mysite/email_notification.html',context)
            subject = "Time to run the monthly aged parts reports"
            email_addresses = ["jesse@dovimotors.com","gordy@dovimotors.com","robin@dovimotors.com","luke@dovimotors.com"]
            send_email(html,subject,email_addresses)

        elif email_type == "parts_45to50":
            part_list =  pa_Get_Parts_Count('detail',-45,-50,'DATEPURC')

            html = part_list.to_html()
            subject = "Get rid of these pronto!  Parts 45 to 50 days old"
            email_addresses = ["jesse@dovimotors.com","gordy@dovimotors.com","robin@dovimotors.com"]
            send_email(html,subject,email_addresses)

        elif email_type == "battery":
            #startdate = datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(-21),'%Y-%m-%d')
            #enddate = datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(-14), '%Y-%m-%d')
            startdate = '2016-08-15'
            enddate = '2016-08-31'
            ro_list = get_service_parts_detail(startdate,enddate)
            ro_list.sort('DATE_OUT')
            html = ro_list.to_html()
            subject = "Battery Cores from %s to %s" % (startdate,enddate)
            email_addresses = ["jesse@dovimotors.com","gordy@dovimotors.com","robin@dovimotors.com"]
            send_email(html,subject,email_addresses)
