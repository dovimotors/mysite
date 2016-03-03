from django.core.management.base import BaseCommand
from dashboard.models import do_conversion

class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        nightly conversion of large tables.
        first item is path to the DBF file, second is the name of the csv to generate.
        """

        file_list = (('\Sicar\Data\\rofile.dbf','rofile.csv'),
                     ('\Sicar\Data\\arcrof.dbf','arcrof.csv'),
                     ('\Sicar\Data\\complain.dbf','complain.csv'),
                     ('\Sicar\Data\\arcomp.dbf','arcomp.csv'),
                     ('\Sicar\Data\\siarctik.dbf','siarctik.csv'),
                 )
        for x,y in file_list:
            do_conversion(x,y)