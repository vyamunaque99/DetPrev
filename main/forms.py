from django import forms


class uploadDatasetForm(forms.Form):
    file = forms.FileField()
