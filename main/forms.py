from urllib import request
from django import forms
from matplotlib import widgets
from .models import Dataset

frecuency_choices =(
    ('Minutos', 'Minutos'),
    ('Horas', 'Horas'),
    ('Dias', 'Dias')
)

class uploadDatasetForm(forms.Form):
    file = forms.FileField()
    

class conformanceCheckingForm(forms.Form):
    def __init__(self,user,*args,**kwargs):
        super(conformanceCheckingForm, self).__init__(*args, **kwargs)
        self.fields['process']=forms.ChoiceField(choices=Dataset.objects.filter(user=user).values_list('name','name'))
        self.fields['process'].widget.attrs.update({'class':'form-control'})
    start_time= forms.TimeField()
    start_date= forms.DateField()
    frecuency= forms.ChoiceField(choices=frecuency_choices)
    frecuency_time= forms.CharField()
    os_user= forms.CharField()
    user_ip= forms.GenericIPAddressField()
    log_file=forms.CharField()
    port_number=forms.CharField()
    ssh_pub_key=forms.CharField(widget=forms.Textarea)
    #Decoradores de forms
    start_time.widget.attrs.update({'class':'form-control input-group-addon'})
    start_date.widget.attrs.update({'class':'form-control'})
    frecuency.widget.attrs.update({'class':'form-control'})
    frecuency_time.widget.attrs.update({'class':'form-control'})
    os_user.widget.attrs.update({'class':'form-control'})
    user_ip.widget.attrs.update({'class':'form-control'})
    log_file.widget.attrs.update({'class':'form-control'})
    port_number.widget.attrs.update({'class':'form-control','value':'22'})
    ssh_pub_key.widget.attrs.update({'class':'form-control'})
    #Inicializacion de clase
    
