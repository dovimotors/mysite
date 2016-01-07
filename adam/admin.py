from django.contrib import admin

# Register your models here.
from .models import ADAMFiles,SGFields

admin.site.register(ADAMFiles)
admin.site.register(SGFields)