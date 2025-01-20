from django.db import models

from django.contrib.auth.models import AbstractUser
LTYPE_CHOICES = [
    ('', 'Select'),
    ('Bsc cs', 'Bsc cs'),
    ('BCA', 'BCA'),
    ('MCA', 'MCA'),
    ('MSC CS', 'MSC CS'),
    ('other', 'other'),



]
department=[
    ('', 'Select'),
    ('IT', 'IT'),
    ('other', 'other'),

]
etype=[
    ('', 'Select'),
    ('single', 'single'),
    ('group', 'group'),

]
class Register(AbstractUser):
    contact = models.IntegerField(null=True)
    realname = models.CharField(max_length=50,default='')

    pin = models.CharField(max_length=50,default='')
    street = models.CharField(max_length=50,default='')
    city = models.CharField(max_length=50,default='')
    collegename=models.CharField(max_length=50,default='')
    department=models.CharField(max_length=50,default='')
    cource=models.CharField(max_length=50,default='')
    admissionnum=models.CharField(max_length=50,default='')
    idproof=models.FileField(null=True)
    gender = models.CharField(max_length=50,default='')
    experience = models.CharField(max_length=50,default=''  )
    qualification = models.CharField(max_length=50,default='')
    usertype = models.IntegerField(null=True)
    dob = models.CharField(max_length=50,default='')
    firm_name = models.CharField(max_length=50,default='')
    firm_type =models.CharField(max_length=50,default='')
    status = models.IntegerField(default=1)
    regno = models.IntegerField(null=True,unique=True)


class Events(models.Model):
    title = models.CharField(max_length=50,default='')
    cod = models.ForeignKey(Register,related_name='cod',on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=500,default='')
    event_type = models.CharField(max_length=500,default='',choices=etype)
    sdate = models.DateField(null=True)
    rules=models.TextField(default='')
    Fees= models.IntegerField(null=True)
    TotalCost=models.IntegerField(null=True)
    stime = models.TimeField(null=True)
    etime = models.TimeField(null=True)
    status=models.IntegerField(null=True,default=1)
    spostatus=models.IntegerField(null=True,default=0)

    first = models.ForeignKey(Register,related_name='f',on_delete=models.CASCADE, null=True)
    second = models.ForeignKey(Register,related_name='s',on_delete=models.CASCADE, null=True)
    third = models.ForeignKey(Register,related_name='t',on_delete=models.CASCADE, null=True)
    sponserid = models.ForeignKey(Register,related_name='sponserid',on_delete=models.CASCADE, null=True)

class feedback(models.Model):
    user_id = models.ForeignKey(Register,related_name='u',on_delete=models.CASCADE, null=True)
    Feedback_msg = models.TextField(default='')
   





    
   