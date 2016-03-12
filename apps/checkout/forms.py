"""Forms used in Checkout app."""
from django import forms
from .models import DeliveryDetails


class DeliveryDetailsForm(forms.ModelForm):
    """Form for taking the delivery details.

    Address to where the product will be delivered.
    """

    name = forms.CharField(
        max_length=254, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required': True}))
    address = forms.CharField(
        max_length=254, required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': '6', 'required': True}))
    phone = forms.CharField(
        min_length=10, max_length=20, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True}))
    zip_code = forms.CharField(
        max_length=10, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True}))

    class Meta:
        """Meta for DeliveryDetailsForm."""

        # DeliveryDetails model
        model = DeliveryDetails
        # excluding the fields that should not be shown in the form
        exclude = [
            'user', 'product', 'order_id', 'timestamp',
            'price', 'quantity', 'total'
        ]

    def clean_phone(self):
        """Validating the phone field."""
        phone = self.cleaned_data.get('phone', None)
        try:
            # the phone field should be a integer only
            int(phone)
        except (ValueError, TypeError):
            raise forms.ValidationError('Please enter a valid phone number')
        return phone


class DeliveryQuantityForm(forms.ModelForm):
    """Form for taking the quantity of the product."""

    quantity = forms.IntegerField(
        required=True, max_value=99, min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'value': '1', 'size': '2', 'min': '1',
            'max': '99', 'required': True
        }))

    class Meta:
        """Meta for Delivery Detail."""

        # UserDetail model
        model = DeliveryDetails

        # Fields to include.
        fields = ["quantity"]
