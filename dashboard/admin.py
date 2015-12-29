from django.contrib import admin

# Register your models here.
from .models import PartsInv, ServiceRO

admin.site.register(PartsInv)
admin.site.register(ServiceRO)
