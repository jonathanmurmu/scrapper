from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    product_type = models.CharField(max_length=30, null=True, blank=True)
    price = models.FloatField(default=0.0, null=True, blank=True)
    landing_url = models.URLField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    scraped_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    site_reference = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
