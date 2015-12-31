from django.core.management.base import BaseCommand
from adam.models import ADAMFiles
from dashboard.models import PartsInv, ServiceRO
import pandas as pd
import datetime
from dbftopandas import AdamImport

class Command(BaseCommand):

    def handle(self, *args, **options):

        ai = AdamImport()

        ifile = 'F:\\adamexports\\adamcache\Incar\Data\INVEN.DBF'
        ofile = 'F:\\adamexports\csvfiles\INVEN.csv'
        out_type = 'csv'


        ai.DBFConverter(ifile,ofile,out_type)

        inv = pd.read_csv(ofile, engine='python')
        ext = inv.ONHAND * inv.COST
        ext = sum(ext)
        try:
            r = PartsInv(invvalue=ext)
            r.save()
            print "updated inventory value to %s" % ext
        except:
            print "There was an error updating invvalue"

        ifile = 'F:\\adamexports\\adamcache\Sicar\Data\\rofile.dbf'
        ofile = 'F:\\adamexports\csvfiles\\rofile.csv'
        out_type = 'csv'

        ai.DBFConverter(ifile,ofile,out_type)

        rof = pd.read_csv(ofile, engine='python')
        cutoff_date = datetime.date.today() + datetime.timedelta(-30)

        ttlcount = rof.RO_NUM.count()
        custsum = rof.CP_TOTAL.sum()
        intsum = rof.IN_TOTAL.sum()
        warsum = rof.WP_TOTAL.sum()
        extsum = rof.XP_TOTAL.sum()

        pcount = rof[rof['STATUS'].str.contains('P')]
        pcount = pcount['STATUS'].count()
        rof['DATE_IN'] = pd.to_datetime(rof['DATE_IN'])

        oldcount = rof[rof['DATE_IN'] < pd.to_datetime(cutoff_date)]
        oldcount = oldcount['RO_NUM'].count()

        try:
            r = ServiceRO(
                totalrocount=ttlcount,
                oldrocount=oldcount,
                printedrocount=pcount,
                ro_custpay=custsum,
                ro_intpay=intsum,
                ro_warpay=warsum,
                ro_extpay=extsum,
            )
            r.save()

            print "updated service RO values"
            print ttlcount, pcount, oldcount, custsum, intsum, warsum, extsum
        except:
            print "There was an error updating Service Ro Values"
