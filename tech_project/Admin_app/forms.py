from django import forms
from .models import *
from Auth_app.models import *



class addeventForm(forms.ModelForm):
   

    class Meta:
        model = Events
        fields = ['title','event_type','description','rules','sdate','stime','etime','Fees','TotalCost']
        widgets = {
            "title" : forms.TextInput(attrs={'class':'contact-input'}),
            "event_type" : forms.Select(attrs={'class':'contact-input','style':'width:100%'}),
            "description" : forms.Textarea(attrs={'class':'contact-input'}),
            "rules" : forms.Textarea(attrs={'class':'contact-input'}),
            "sdate" : forms.DateInput(attrs={'class':'contact-input','type':'date'}),
            "stime" : forms.TimeInput(attrs={'class':'contact-input','type':'time'}),
            "etime" : forms.TimeInput(attrs={'class':'contact-input','maxlength':'10','type':'time'}),
            "Fees" : forms.NumberInput(attrs={'class':'contact-input'}),
            "TotalCost" : forms.NumberInput(attrs={'class':'contact-input'}),

        } 
        labels={
            'sdate' :' Date',
            'stime' :'Start Time',
            'etime' :'End Time',

        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sdate'].required = False


class addecorationsForm(forms.ModelForm):
    class Meta:
        model = decorations
        fields = ['title','dec','amount']
        widgets = {
            "title" : forms.TextInput(attrs={'class':'contact-input'}),
            "dec" : forms.FileInput(attrs={'class':'contact-input'}),
            "amount" : forms.NumberInput(attrs={'class':'contact-input','style':'width:100%'}),
        } 
        labels={
            'title' :'Title',
            'dec' :' Decoration Image',
            'amount' :'Amount',
        }