from django.db import models

# Create your models here.


class PartsInv(models.Model):

    #def __str__(self):
    #   return self.statdate

    statdate = models.DateField(auto_now=True)
    invvalue = models.FloatField()

class ServiceRO(models.Model):

    statdate = models.DateField(auto_now=True)
    totalrocount = models.IntegerField()
    oldrocount = models.IntegerField()
    printedrocount = models.IntegerField()
    ro_custpay = models.FloatField()
    ro_intpay = models.FloatField()
    ro_warpay = models.FloatField()
    ro_extpay = models.FloatField()
