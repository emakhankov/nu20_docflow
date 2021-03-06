from django import forms

from usersapp.models import DocFlowUser
from .models import DocumentType, Document, Counterpart, Classifier, Task
from django.conf import settings

class SearchForm(forms.Form):
    # можно так
    # forms.ChoiceField(choices=[
    #    (choice.pk, choice) for choice in MyChoices.objects.all()])

    type = forms.ModelChoiceField(label='Тип документа', required=False, queryset=DocumentType.objects.all())
    nom = forms.CharField(label='Номер', required=False)
    date_from = forms.DateField(label='Дата документа с', required=False, input_formats=['%d.%m.%Y', ],)
    date_to = forms.DateField(label='Дата документа по', required=False, input_formats=['%d.%m.%Y', ],)
    description = forms.CharField(label='Описание', required=False)

    all = forms.CharField(label='Описание', required=False, widget=forms.HiddenInput())


class DocumentAddEditForm(forms.ModelForm):

    type = forms.ModelChoiceField(label='Тип документа', required=True, queryset=DocumentType.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    nom = forms.CharField(label='Номер документа', required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    date = forms.DateField(label='Дата документа', required=True, input_formats=['%d.%m.%Y', ],
                           widget=forms.DateInput(attrs={'class': 'form-control'}))

    counterpart = forms.ModelMultipleChoiceField(label='Контрагенты', required=False,
                                                 queryset=Counterpart.objects.all(),
                                                 widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    description = forms.CharField(label='Описание', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    classifier = forms.ModelMultipleChoiceField(label='Классификаторы', queryset=Classifier.objects.all(),
                                                widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Document
        # fields = '__all__'
        fields = ('type', 'nom', 'date', 'counterpart', 'description', 'classifier')
        # exclude = ('tags',)


class TaskAddEditForm(forms.ModelForm):

    name = forms.CharField(label='Задача', required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    date = forms.DateField(label='Дата задачи', required=True, input_formats=['%d.%m.%Y', ],
                           widget=forms.DateInput(attrs={'class': 'form-control datepicker'}))

    #date = forms.DateField(widget=forms.SelectDateWidget(years=last_years()))

    user_to = forms.ModelChoiceField(label='Направить', required=True, queryset=DocFlowUser.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:

        model = Task
        fields = ('name', 'description', 'date', 'user_to')


class CounterpartAddEditForm(forms.ModelForm):

    name = forms.CharField(label='Наименование', required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='Полное наименование', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    tax_number = forms.CharField(label='ИНН', required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:

        model = Counterpart
        fields = ('name', 'full_name', 'tax_number')