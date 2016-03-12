"""Model for checkout."""
from django.db import models
from django.contrib.auth.models import User
from apps.home.models import Product


class DeliveryDetails(models.Model):
    """Model for storing the details of the order.

    The billing address, user id, product id.
    """

    # the logged in user who is ordering the product
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
    )
    # the id of the product which is been ordered.
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
    )

    order_id = models.CharField(max_length=20, blank=True)

    # shipping address
    name = models.CharField(max_length=254, null=True, blank=True)
    address = models.CharField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)

    # time when the order is placed
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # no of items ordered
    quantity = models.IntegerField(default=1)

    # price of the product ordered
    price = models.FloatField(null=True, blank=True)

    # total price of the product (qunatity * price)
    total = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Calculating the total payable amount."""
        self.total = self.quantity * self.price
        super(DeliveryDetails, self).save(*args, **kwargs)

    def __str__(self):
        """Value to return if object is called."""
        return self.order_id
