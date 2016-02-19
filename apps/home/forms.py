"""Forms used in scrapper project."""
from django import forms
from apps import constants


class ScrapSearchForm(forms.Form):
    """Search form to scrap items."""

    search = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True}))
    site = forms.ChoiceField(
        choices=constants.SITE_CHOICES, required=True,
        widget=forms.RadioSelect(attrs={'required': True}))


class DashboardSearchForm(forms.Form):
    """Search form to search products in the dashboard."""
    search = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True}))
