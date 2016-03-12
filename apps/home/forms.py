"""Forms used in dashboard.

Scrap form, dashboard search form, filter form used in the dashboard page.
"""
from django import forms
from apps import constants


class ScrapSearchForm(forms.Form):
    """Search form to scrap items."""

    # search textbox
    search = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True
        })
    )
    # radio button to select website
    site_choice = forms.ChoiceField(
        choices=constants.SITE_CHOICES, required=True,
        widget=forms.RadioSelect(attrs={'required': True})
    )


class DashboardSearchForm(forms.Form):
    """Search form to search products in the dashboard from the database."""

    # search textbox
    search = forms.CharField(
        max_length=255, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control sharp-corner-right', 'required': True,
            'placeholder': 'What would you like to search?'
        })
    )


class DashboardFilterForm(forms.Form):
    """Search products from database.

    It provide all the fields needed for search form.
    """

    # Radio fields.
    price_sort = forms.ChoiceField(
        required=False, choices=constants.PRICE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'filter-click',
            'required': False
        })
    )

    # Checkbox fields.
    amazon = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'filter-click'})
    )
    flipkart = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'filter-click'})
    )
