from django import forms


class uploadDatasetForm(forms.Form):
    dataset_name = forms.CharField(label='Nombre del dataset', max_length=30)
    file = forms.FileField(label='Archivo')
