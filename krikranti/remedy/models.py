from django.db import models


# Create your models here.
class Remedy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    remedy = models.CharField(max_length=1500)

    def __str__(self):
        return self.name
