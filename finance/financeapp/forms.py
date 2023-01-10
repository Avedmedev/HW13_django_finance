import datetime

from django import forms
from django.contrib.admin import widgets

from .models import CashIn, CashOut, Contractor


class CashInForm(forms.ModelForm):

    class Meta:
        model = CashIn
        fields = '__all__'
        exclude = ['user', 'transacted']


class CashOutForm(forms.ModelForm):

    class Meta:
        model = CashOut
        fields = '__all__'
        exclude = ['user', 'transacted']


class ReportForm(forms.Form):
    start = forms.DateField(
        widget=forms.SelectDateWidget(years=[i for i in range(2019, 2025)]),
        initial=datetime.datetime.now() - datetime.timedelta(days=365))
    end = forms.DateField(
        widget=forms.SelectDateWidget(years=[i for i in range(2019, 2025)]),
        initial=datetime.datetime.now() + datetime.timedelta(days=365)
    )
    in_out = forms.ChoiceField(widget=forms.Select, choices=(('opt1', 'in_out'), ('opt2', 'in'), ('opt3', 'out')))


class ContractorForm(forms.ModelForm):
    name = forms.ModelMultipleChoiceField(
        widget=widgets.FilteredSelectMultiple(verbose_name='Contractors', is_stacked=True),
        queryset=Contractor.objects.all()
    )

    class Meta:
        model = Contractor
        fields = ['name']
        # name = forms.MultiValueField
