"""Views for checkout app.

This view stores the billing address. Displays the summary of the product
ordered, billing address and the total payment amount.
This view also makes payment using the Strip payment processing api. And the
finally displays that  the ordered is placed successfully.
"""
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from apps.checkout.forms import DeliveryDetailsForm
import stripe
import random
from .models import DeliveryDetails
from .forms import DeliveryQuantityForm
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import json
import logging
from apps import constants


stripe.api_key = settings.STRIPE_SECRET_KEY


class DeliveryDetailsView(TemplateView):
    """View for taking the delivery details.

    Stores the delivery address in the database.
    """

    template_name = 'checkout/delivery_address.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for DeliveryDetailsView."""
        # if the cache does not have product id and user is trying to access
        # this view's html page then redirect it to dashboard page.
        if not cache.get('product_id'):
            return HttpResponseRedirect(reverse('dashboard'))
        form = DeliveryDetailsForm()

        # creating the context
        ctx = {'title': 'Checkout', 'form': form, 'dashboard': 'active'}

        # rendering the template
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Post method for DeliveryDetailsView."""
        form = DeliveryDetailsForm(request.POST)
        logger = logging.getLogger(constants.LOGGER)

        # id of the selected product
        product_id = cache.get('product_id')

        # checking if the form is valid
        if form.is_valid():
            data = form.cleaned_data

            # generating a 10 digit random number for the order id
            order_id = 'OD' + str(random.randint(1000000000, 9999999999))

            # getting the price of the selected product from the cache
            price = cache.get('price')

            # id of the logged in user
            user_id = request.user.pk

            # storing the delivery address in the database
            try:
                # creating the dictionary
                data = {
                    'name': data['name'], 'address': data['address'],
                    'phone': data['phone'], 'zip_code': data['zip_code'],
                    'order_id': order_id, 'user_id': user_id,
                    'product_id': product_id, 'price': price
                }

                # storing the address details in the database
                order = DeliveryDetails.objects.create(**data)

                # storing the order id in the cache
                cache.set('order', order, None)

                # redirecting to summary view
                return HttpResponseRedirect(reverse('summary'))
            except Exception as e:
                logger.exception("Error: " + e)
        else:
            logger.error("Form is not valid.")

            # creating the context
            ctx = {'title': 'Delivery', 'form': form}

            # rendering the template
            return render(request, self.template_name, ctx)

        # creating the context
        ctx = {'title': 'Checkout', 'dashboard': 'active'}

        # rendering the template
        return render(request, self.template_name, ctx)


class SummaryView(TemplateView):
    """Class for SummaryView."""

    template_name = 'checkout/summary.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for SummaryView."""
        # if the cache does not have order and user is trying to access this
        # view's html page then redirect it to dashboard page.
        if not cache.get('order'):
            return HttpResponseRedirect(reverse('dashboard'))
        form = DeliveryQuantityForm()

        # setting the total price in the price
        cache.set('total_price', cache.get('price'), None)

        # creating the context
        ctx = {
            'title': 'Checkout', 'dashboard': 'active', 'form': form,
            'product_id': cache.get('product_id'), 'order': cache.get('order')
        }

        # rendering the template
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Post method for SummaryView class."""
        form = DeliveryQuantityForm(request.POST)
        logger = logging.getLogger(constants.LOGGER)

        # for holding the json tha will be send to the template as response
        json_data = {}

        # update the quantity and the total price, when the quantity is changed
        # getting the order stored in the cache
        order = cache.get('order')

        # cheecking the form is valid or not
        if form.is_valid():
            data = form.cleaned_data
            try:
                quantity = DeliveryDetails.objects.filter(pk=order.id)

                # updating the quatity
                quantity.update(**data)

                # this will update the total price (quantity * price)
                quantity[0].save()

                # setting the total price in the price
                cache.set('total_price', quantity[0].total, None)

                # data to send as json response
                json_data = {'total_price': quantity[0].total, 'success': True}

                # sending the json response
                return HttpResponse(
                    json.dumps(json_data), content_type='application/json')
            except Exception as e:
                logger.exception("Error: " + e)
        else:
            logger.exception("Form is not valid.")

            # data to send as json response
            json_data = {'success': False}
            json_data = {'message': "Quantity should be between 0 and 99."}

            # sending the json response
            return HttpResponse(
                json.dumps(json_data), content_type='application/json')

        # creating the context and rendering the template
        ctx = {'title': 'Checkout', 'form': form}
        return render(request, self.template_name, ctx)


class PaymentView(TemplateView):
    """Class for the payment view."""

    template_name = 'checkout/payment.html'
    publish_key = settings.STRIPE_PUBLISHABLE_KEY

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for CheckoutView class."""
        # if the cache does not have order and user is trying to access this
        # view's html page then redirect it to dashboard page.
        if not cache.get('order'):
            return HttpResponseRedirect(reverse('dashboard'))

        # creating the context and rendering the form
        ctx = {
            'title': 'Checkout', 'publish_key': self.publish_key,
            'dashboard': 'active'
        }
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Post method for CheckoutView class."""
        # the stripe api sends this stripeToken after validating the card
        token = request.POST['stripeToken']

        # Create the charge on Stripe's servers,
        # this will charge the user's card
        total_price = cache.get('total_price')
        try:
            charge = stripe.Charge.create(
                amount=int(total_price * 100),  # amount in paise
                currency="inr",
                source=token,
                description="Example charge"
            )

            # clearing the cache (price, order, total), when payment is done
            cache.clear()

            # create the context and render the template
            ctx = {'title': 'Checkout', 'success': True, 'dashboard': 'active'}
            return render(request, self.template_name, ctx)
        except stripe.error.CardError:
            # The card has been declined
            logger = logging.getLogger(constants.LOGGER)
            logger.error("Card has been cancled, order declined.")

            # creating the context and rendering the template
            ctx = {'title': 'Checkout', 'error': True, 'dashboard': 'active'}
            return render(request, self.template_name, ctx)

        ctx = {
            'title': 'Checkout', 'publish_key': self.publish_key,
            'dashboard': 'active'
        }
        return render(request, self.template_name, ctx)
