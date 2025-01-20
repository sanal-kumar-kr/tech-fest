from django import forms
from .models import *

from Auth_app.models import *

        
class Feedbackform(forms.ModelForm):
    
    class Meta:
        model = feedback
        fields = ['Feedback_msg']
        widgets = {
            "Feedback_msg" : forms.Textarea(attrs={'class':'form-input','style':'width : 90%;'}),
        }


class groupform(forms.ModelForm):
    
    class Meta:
        model = group
        fields = ['member2','member3','member4']
        widgets = {
            "member2" : forms.TextInput(attrs={'class':'form-input','style':'width : 100%;'}),
            "member3" : forms.TextInput(attrs={'class':'form-input','style':'width : 100%;'}),
            "member4" : forms.TextInput(attrs={'class':'form-input','style':'width : 100%;'}),
        }

class PaymentForm(forms.Form):
    fee = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'style-input'}))
    CardNumber = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'style-input','placeholder':'Enter 16 digit'}))
    CVV = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'style-input','placeholder':'CVV'}))
    ExpiryDate = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'style-input','placeholder':"MM/YY"}))
 
    
       
    
    