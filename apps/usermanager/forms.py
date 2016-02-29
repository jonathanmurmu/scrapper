"""Forms for Usermanager app.

Signup, login and edit profile form.
"""
from django import forms
from .models import UserDetail
from apps import constants


class SignUpForm(forms.Form):
    """Sign up form.

    Form for registering the user.
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
    """Login Form."""

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
    """Form for editing the profile."""

    # textboxes
    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False})
    )

    # radio button
    gender = forms.ChoiceField(
        choices=constants.GENDER_CHOICES, required=False,
        widget=forms.RadioSelect(attrs={'required': False}))

    # textboxes
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'date', 'class': 'form-control'}))

    # dropdown box
    marital = forms.ChoiceField(
        choices=constants.MARITAL_CHOICES, required=False)

    # textboxes
    phone = forms.CharField(
        required=False, max_length=20, min_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))

    # textarea
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 3}))

    # textboxes
    street = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))
    state = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))
    zip_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'required': False}))

    # checkboxes
    mail = forms.BooleanField(required=False)
    message = forms.BooleanField(required=False)
    phonecall = forms.BooleanField(required=False)
    other = forms.BooleanField(required=False)
    extra_note = forms.CharField(
        required=False, widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 3}))

    # image field
    image = forms.ImageField(required=False)

    class Meta:
        """Meta for UserDetail."""

        # UserDetail model
        model = UserDetail
        # specifying the fields to be shown in the form
        fields = [
            'first_name', 'last_name', 'gender', 'date_of_birth',
            'marital', 'phone', 'address', 'street', 'city', 'state',
            'zip_code', 'mail', 'message', 'phonecall', 'other', 'extra_note',
            'image'
        ]

    def clean_phone(self):
        """Validating the phone field."""
        phone = self.cleaned_data.get('phone', None)
        try:
            int(phone)
        except (ValueError, TypeError):
            raise forms.ValidationError('Please enter a valid phone number')
        return phone

    def __init__(self, request, *args, **kwargs):
        """Setting initial value for fields."""
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # from auth_user table
        self.fields['first_name'].initial = request.user.first_name
        self.fields['last_name'].initial = request.user.last_name

        # from userdetial table
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
