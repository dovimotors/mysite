from django.core.management.base import BaseCommand
from dashboard.models import DailyMetrics, pa_Get_Inventory_Value,pa_Get_Parts_Count, sv_Get_RO_Count


class Command(BaseCommand):

    def handle(self, *args, **options):
        invvalue = pa_Get_Inventory_Value()
        inv30to45 = pa_Get_Parts_Count('total',-29,-45)
        inv60to65 = pa_Get_Parts_Count('total',-59,-65)
        rocount = sv_Get_RO_Count(type='totalcount')
        oldcount = sv_Get_RO_Count(type='oldcount')
        dm = DailyMetrics(
            pa_invvalue = invvalue,
            sv_ro_count = rocount,
            sv_old_ro_count = oldcount,
            pa_count30to45 = inv30to45,
            pa_count60to65 = inv60to65
        )
        dm.save()