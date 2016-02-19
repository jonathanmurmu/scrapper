from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('1', 'Male'),
    ('2', 'Female'),
)
MARITAL_CHOICES = (
    ('1', 'Single'),
    ('2', 'Married'),
)
def generate_filename(self, filename):
    """Used for handling upload file."""

    url = "static/uploads/%s/%s" % (self.pk, filename)
    return url


class UserDetail(models.Model):
    # one-to-one relation with the auth_user table
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    marital = models.CharField(max_length=1, choices=MARITAL_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    # address fields
    address = models.CharField(max_length=254, null=True, blank=True)  # textarea in form
    street = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    zip_code = models.CharField(max_length=6, null=True, blank=True)
    # contact field
    phone = models.IntegerField(null=True, blank=True)
    # extra note field (textarea in form)
    extra_note = models.CharField(max_length=254, null=True, blank=True)
    # prefered communication (checkbox fields in form)
    mail = models.BooleanField(default=False)
    message = models.BooleanField(default=False)
    phonecall = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    # profile pic field
    image = models.ImageField(upload_to='static/uploads/', null=True, blank=True)

    def __str__(self):
        return self.city
