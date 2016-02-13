from django.core.management.base import BaseCommand
from dashboard.models import do_conversion

class Command(BaseCommand):

    def handle(self, *args, **options):
        file_list = (('\Sicar\Data\\rofile.dbf','rofile.csv'),
                     ('\Sicar\Data\\arcrof.dbf','arcrof.csv'),
                 )
        for x,y in file_list:
            do_conversion(x,y)