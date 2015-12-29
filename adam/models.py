from django.db import models
from django.conf import settings

# Create your models here.
class ADAMFiles(models.Model):
    def __str__(self):
        return self.DBFPath



    DBFPath = models.FilePathField(
        path=settings.ADAM_PATH,
        recursive=True,
    )



