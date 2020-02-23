from django import forms


class SearchForm(forms.Form):

    nom = forms.CharField(label='Название', required=False)
    date_from = forms.DateField(label='Дата документа с', required=False)
    date_to = forms.DateField(label='Дата документа по', required=False)
    desription = forms.CharField(label='Описание', required=False)