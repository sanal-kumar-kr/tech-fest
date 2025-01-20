from django import forms
from .models import *

class photoForm(forms.ModelForm):
    class Meta:
        model = sponserdecorations
        fields = ['adphoto']
        widgets = {
            "adphoto" : forms.FileInput(attrs={'class':'form-input','style':'width : 100%;'}),
        
        }