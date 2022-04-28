from urllib import request
from django import forms
from matplotlib import widgets
from .models import Dataset, Stakeholder, StakeholderList, StakeholderListDetail

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
        self.fields['stakeholder_list']=forms.ChoiceField(choices=StakeholderList.objects.all().values_list('id','name'))
        self.fields['stakeholder_list'].widget.attrs.update({'class':'form-control'})
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

class stakeholderForm(forms.ModelForm):
    name=forms.CharField()
    email=forms.EmailField()
    #Decoradores de forms
    name.widget.attrs.update({'class':'form-control'})
    email.widget.attrs.update({'class':'form-control'})
    class Meta:
            model = Stakeholder
            fields = '__all__'

class stakeholderListForm(forms.ModelForm):
    name=forms.CharField()
    #Decoradores de forms
    name.widget.attrs.update({'class':'form-control'})
    class Meta:
            model = StakeholderList
            fields = '__all__'

class stakeholderListDetailForm(forms.ModelForm):
    #def __init__(self,user,*args,**kwargs):
    #    super(stakeholderListDetailForm,self).__init__(*args, **kwargs)
    stakeholder_list=forms.ModelChoiceField(queryset=StakeholderList.objects.all(),empty_label=None)
    stakeholder=forms.ModelChoiceField(queryset=Stakeholder.objects.all(),empty_label=None)
    #Decoradores de forms
    stakeholder_list.widget.attrs.update({'class':'form-control'})
    stakeholder.widget.attrs.update({'class':'form-control'})
    class Meta:
            model = StakeholderListDetail
            fields = '__all__'
