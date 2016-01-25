from django.core.management.base import BaseCommand
import sendgrid
from dashboard.models import pa_Get_Parts_Count
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

            message.add_to(["jesse@dovimotors.com","gordy@dovimotors.com"])
            message.set_from_name("Dovi Motors Inc.")
            message.set_from("admin@dovimotors.com")
            message.set_subject(subject)
            message.set_html(htmlbody)

            status, msg = sg.send(message)

            return (status,msg)

        part_list =  pa_Get_Parts_Count('detail',-29,-45,'DATEPURC')
        html = part_list.to_html()
        subject = "Parts 30 to 45 days old"
        send_email(html,subject)
