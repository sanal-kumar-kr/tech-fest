from django.db import models
from Auth_app.models import *
# Create your models here.
class Registevevnts(models.Model):
    user_id = models.ForeignKey(Register,related_name='user',on_delete=models.CASCADE, null=True)
    card = models.ImageField(blank=True, null=True)
    evnt_id = models.ForeignKey(Events,related_name='e',on_delete=models.CASCADE, null=True)



class group(models.Model):
    user_id = models.ForeignKey(Register,related_name='gp',on_delete=models.CASCADE, null=True)
    evnt_id = models.ForeignKey(Events,related_name='esdfsd',on_delete=models.CASCADE, null=True)

    member2=models.CharField(max_length=500,default='')
    member3=models.CharField(max_length=500,default='')
    member4=models.CharField(max_length=500,default='')

