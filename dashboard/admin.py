from django.contrib import admin

# Register your models here.
from .models import PartsInv, ServiceRO, DailyMetrics

admin.site.register(PartsInv)
admin.site.register(ServiceRO)
admin.site.register(DailyMetrics)
