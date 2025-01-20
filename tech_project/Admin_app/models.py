from django.db import models
from Auth_app.models import *
# Create your models here.
class certificatese(models.Model):
    user_id = models.ForeignKey(Register,related_name='usercert',on_delete=models.CASCADE, null=True)
    card = models.ImageField(blank=True, null=True)
    evnt_id = models.ForeignKey(Events,related_name='evt',on_delete=models.CASCADE, null=True)


class decorations(models.Model):
    title = models.CharField(max_length=50,default='')
    dec= models.FileField(null=True)
    amount= models.IntegerField(null=True)
    year= models.IntegerField(null=True)
    status=models.IntegerField(null=True,default=0)
