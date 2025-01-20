from django import forms
from .models import *


        
class LoginForm(forms.ModelForm):
    
    class Meta:
        model = Register
        fields = ['username','password']
        widgets = {
            "username" : forms.TextInput(attrs={'class':'form-input','style':'width : 90%;',"placeholder":"Username"}),
            "password" : forms.PasswordInput(attrs={'class':'form-input','style':'width : 90%;',"placeholder":"Password"})
        }
        help_texts = {
            'username' : None
        }
    
        
GENDER_CHOICES=[
    ('',' Select'),
    ('male',' male'),
    ('female',' female'),
    ('other',' other')
]


class StaffRegisterForm(forms.ModelForm): 
    class Meta:
        model = Register
        fields = ['username','email','password','contact','idproof','cource']
        widgets = {
            "username" : forms.TextInput(attrs={'class':'contact-input'}),
            "email" : forms.EmailInput(attrs={'class':'contact-input'}),
            "password" : forms.PasswordInput(attrs={'class':'contact-input'}),
            "contact" : forms.TextInput(attrs={'class':'contact-input','maxlength':'10'}),
            "idproof" : forms.FileInput(attrs={'class':'contact-input'}),
            "cource" : forms.TextInput(attrs={'class':'contact-input'}),
        }    
            
    def __init__(self, *args, **kwargs):
            super(StaffRegisterForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.required = False
       
class StudentRegisterForm(forms.ModelForm):
   
    class Meta:
        model = Register
        fields = ['username','email','password','contact','admissionnum','idproof','department','cource']
        widgets = {

            "username" : forms.TextInput(attrs={'class':'contact-input'}),
            "email" : forms.EmailInput(attrs={'class':'contact-input'}),
            "password" : forms.PasswordInput(attrs={'class':'contact-input'}),
            "contact" : forms.TextInput(attrs={'class':'contact-input','maxlength':'10'}),
            "admissionnum" : forms.TextInput(attrs={'class':'contact-input','maxlength':'10'}),
            "idproof" : forms.FileInput(attrs={'class':'contact-input'}),
            "department" : forms.TextInput(attrs={'class':'contact-input'}),
            "cource" : forms.TextInput(attrs={'class':'contact-input'}),

        }   
    def __init__(self, *args, **kwargs):
            super(StudentRegisterForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.required = False    

class SponserRegisterForm(forms.ModelForm):
   

    class Meta:
        model = Register
        fields = ['username','email','password','contact','firm_name','pin','street','city','firm_type','idproof']
        widgets = {

            "username" : forms.TextInput(attrs={'class':'contact-input'}),
            "email" : forms.EmailInput(attrs={'class':'contact-input'}),
            "password" : forms.PasswordInput(attrs={'class':'contact-input'}),
            "contact" : forms.TextInput(attrs={'class':'contact-input','maxlength':'10'}),
            "firm_name" : forms.TextInput(attrs={'class':'contact-input'}),
            "pin" : forms.TextInput(attrs={'class':'contact-input'}),
            "street" : forms.TextInput(attrs={'class':'contact-input'}),
            "city" : forms.TextInput(attrs={'class':'contact-input'}),
            "idproof" : forms.FileInput(attrs={'class':'contact-input'}),
            "firm_type" : forms.TextInput(attrs={'class':'contact-input'})

        }   
    def __init__(self, *args, **kwargs):
            super(SponserRegisterForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.required = False         



                      

