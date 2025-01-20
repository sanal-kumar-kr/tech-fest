from django.db import models
from Auth_app.models import *
from Admin_app.models import *

# Create your models here.

class sponserevent(models.Model):
    user_id = models.ForeignKey(Register,related_name='sid',on_delete=models.CASCADE, null=True)
    card = models.ImageField(blank=True, null=True)
    evnt_id = models.ForeignKey(Events,related_name='esid',on_delete=models.CASCADE, null=True)


class sponserdecorations(models.Model):
    user_id = models.ForeignKey(Register,related_name='sdecid',on_delete=models.CASCADE, null=True)
    adphoto=models.FileField(null=True)
    decid = models.ForeignKey(decorations,related_name='edecsid',on_delete=models.CASCADE, null=True)
    card=models.FileField(null=True)

