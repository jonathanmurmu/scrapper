"""Forms used in scrapper project."""
from django.contrib.auth.models import User
from django import forms
from .models import UserDetail
from apps import constants
from django.forms import extras


class SignUpForm(forms.Form):
    """Sign up form.

    Form for register the user.
    """

    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True}))
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True})
    )
    email = forms.EmailField(
        max_length=254, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True})
    )
    username = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True})
    )
    password = forms.CharField(
        max_length=128, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'required': True})
    )
    confirm_password = forms.CharField(
        max_length=128, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'required': True})
    )


class LoginForm(forms.Form):
    """docstring for LoginForm."""

    username = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': True})
    )
    password = forms.CharField(
        max_length=128, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'required': True})
    )


class EditProfileForm(forms.ModelForm):
    """Edit profile page."""

    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False})
    )
    gender = forms.ChoiceField(
        choices=constants.GENDER_CHOICES, required=False,
        widget=forms.RadioSelect(attrs={'required': False}))
    date_of_birth = forms.DateField(
        required=False, widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}))
    marital = forms.ChoiceField(choices=constants.MARITAL_CHOICES, required=False)
    phone = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    street = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}))
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}))
    zip_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}))
    mail = forms.BooleanField(required=False)
    message = forms.BooleanField(required=False)
    phonecall = forms.BooleanField(required=False)
    other = forms.BooleanField(required=False)
    extra_note = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    image = forms.ImageField(required=False)


    class Meta:

        model = UserDetail
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth', 'marital', 'phone', 'address', 'street', 'city', 'state', 'zip_code', 'mail', 'message', 'phonecall', 'other', 'extra_note', 'image']
        # fields = ['first_name', 'last_name', 'gender']
        # exclude = ['user_id', 'id']

    def __init__(self, request, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # import pdb
        # pdb.set_trace()
        self.fields['first_name'].initial = request.user.first_name
        self.fields['last_name'].initial = request.user.last_name
        ud = UserDetail.objects.get(user=request.user)
        self.fields['gender'].initial = ud.gender
        self.fields['date_of_birth'].initial = ud.date_of_birth
        self.fields['marital'].initial = ud.marital
        self.fields['phone'].initial = ud.phone
        self.fields['address'].initial = ud.address
        self.fields['street'].initial = ud.street
        self.fields['city'].initial = ud.city
        self.fields['state'].initial = ud.state
        self.fields['zip_code'].initial = ud.zip_code
        self.fields['mail'].initial = ud.mail
        self.fields['message'].initial = ud.message
        self.fields['phonecall'].initial = ud.phonecall
        self.fields['other'].initial = ud.other
        self.fields['extra_note'].initial = ud.extra_note

    def save():
        pass
