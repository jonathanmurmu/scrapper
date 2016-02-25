"""Defining the constants used in the project."""
GENDER_CHOICES = (
    ('1', 'Male'),
    ('2', 'Female'),
)
MARITAL_CHOICES = (
    ('1', 'Single'),
    ('2', 'Married'),
)

FLIPKART_URL = "http://www.flipkart.com"
AMAZON_URL = "http://www.amazon.in/"

SITE_CHOICES = (
    ('1', 'amazon.in'),
    ('2', 'flipkart.com'),
)

SITE_REFERENCE_FLIPKART = 'flipkart'
SITE_REFERENCE_AMAZON = 'amazon'

# for sending email
EMAIL_HOST = 'email.mindfiresolutions.com'
EMAIL_HOST_USER = 'jonathan.murmu@mindfiresolutions.com'
EMAIL_HOST_PASSWORD = 'jono0077'

# for acitvating the user
ACTIVATION_URL = "http://localhost:8000/activate/"
