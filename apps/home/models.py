"""Model used for scrapping items and storing in the database."""
from django.db import models
from django.template.defaultfilters import slugify


class Product(models.Model):
    """Model for storing the details of the product."""

    # details of the product, the date on which it is scrapped,
    # the website where the product is being sold, and the product's slug name
    name = models.CharField(max_length=255, null=True, blank=True)
    product_type = models.CharField(max_length=30, null=True, blank=True)
    price = models.FloatField(default=0.0, null=True, blank=True)
    landing_url = models.URLField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    scraped_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    site_reference = models.CharField(max_length=50, null=True, blank=True)
    slug_name = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self):
        """Value to return if object is called."""
        return self.name

    def save(self, *args, **kwargs):
        """Slugifying the name field."""
        self.slug_name = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
