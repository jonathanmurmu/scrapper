"""View for the home page.

Home page view, dashboard view, filter in dashboard, displaying the
product page profile page and edit page.
"""
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.usermanager import forms
from django.contrib.auth.models import User
from apps.usermanager.models import UserDetail
from django.conf import settings
import os
from apps.home.scrap import Scrap
from apps.home.forms import ScrapSearchForm
from apps.home.forms import DashboardSearchForm
from apps.home.forms import DashboardFilterForm
from apps.home.models import Product
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
import logging
from apps import constants
import json
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class HomeView(TemplateView):
    """Class for the home page view."""

    template_name = 'home/home.html'

    def get(self, request, *args, **kwargs):
        """Get method for HomeView class."""
        ctx = {'title': 'Home', 'home': 'active'}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        """Post method for HomeView class."""
        pass


class DashboardView(TemplateView):
    """View for the dashboard.

    Allows user to search for the product,
     and display the result in the front end.
    The results are fetched from the database.
    """

    template_name = 'home/dashboard.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for DashboardView class."""
        products = []
        result_error = ""
        if request.is_ajax():
            # search form
            form = DashboardSearchForm(request.GET)
            # filter form
            form2 = DashboardFilterForm(request.GET)

            if form.is_valid():
                data = form.cleaned_data
                search_item = data['search']

                # getting the products whose name or price or site reference or
                # product type or description matches with the search item
                products = Product.objects.filter(
                    Q(name__icontains=search_item) |
                    Q(price__icontains=search_item) |
                    Q(site_reference__icontains=search_item) |
                    Q(product_type__icontains=search_item) |
                    Q(description__icontains=search_item)
                )

                # when resuts are found initial 'resutl' variable
                if products:
                    result = products
                # otherwise initialize error message
                else:
                    result = None
                    result_error = True

                # storing the searched result in the cache,
                # in order to use it in the DashboardFilterView
                cache.set('product_result', result, None)

                # create a dictionary to hold the result and the error feedback
                ctx = {
                    'result': result, 'dashboard_result_error': result_error}
                html = render_to_string(
                    'home/result.html', ctx,
                    context_instance=RequestContext(request))
                # encoding it to json
                json_data = json.dumps({'result': html})
                # sending the json response
                return HttpResponse(json_data, content_type='application/json')
        else:
            form = DashboardSearchForm()
            form2 = DashboardFilterForm()

        # create a dictionary for the context
        ctx = {
            'title': 'Dashboard', 'dashboard': 'active', 'form': form,
            'result': products, 'result_error': result_error, 'form2': form2
        }
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Post method for DashboardView class."""
        pass


class DashboardFilterView(TemplateView):
    """View for filtering the results in the dashboard.

    The results can be filtered according to price, site choice etc.
    """

    template_name = 'home/dashboard.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Filtering the results based on price, site choice etc."""
        result_error = ""
        # storing the search results in 'results' and applying filters to it'
        result = cache.get('product_result')
        if request.is_ajax():
            form2 = DashboardFilterForm(request.GET)
            if form2.is_valid():
                filter_data = form2.cleaned_data
                if result:
                    # sorting price of the result in ascending order
                    if filter_data['price_sort'] == 'LH':
                        result = result.order_by('price')
                    # sorting price of the result in descending order
                    elif filter_data['price_sort'] == 'HL':
                        result = result.order_by('-price')

                    # filtering the results for both amazon and flipkart,
                    # i.e when user check both flipkart and amzon
                    if filter_data['amazon'] and filter_data['flipkart']:
                        pass
                    # filtering the results which are only from amazon
                    elif filter_data['amazon']:
                        result = result.filter(
                            Q(site_reference__icontains='amazon'))
                    # filtering the results which are only from flipkart
                    elif filter_data['flipkart']:
                        result = result.filter(
                            Q(site_reference__icontains='flipkart'))

                # when no results are found, display the error message,
                # set the result error flag to true
                else:

                    # make result to none.
                    result = None
                    result_error = True

            else:
                logger = logging.getLogger(constants.LOGGER)
                logger.error("Wrong data")

            # create the context
            ctx = {'result': result, 'dashboard_result_error': result_error}
            html = render_to_string(
                'home/result.html', ctx,
                context_instance=RequestContext(request))
            # encoding it to json
            json_data = {'result': html}
            # sending the json response
            return HttpResponse(
                json.dumps(json_data), content_type='application/json')

        # Contexts to send in html.
        ctx = {
            'title': 'Dashboard page', 'dashboard': 'active',
            'form2': form2}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        """Post method for DashboardFilterView."""
        pass


class ProductDisplayView(TemplateView):
    """View to display the product detail."""

    template_name = 'home/product_display.html'

    @method_decorator(login_required)
    def get(self, request, name, *args, **kwargs):
        """Get method for ProductDisplayView class."""
        # fetching the product from the given slug name of the product
        product = Product.objects.filter(slug_name=name)
        try:
            # fetching the product id of the selected product
            pk = product[0].pk
        except:
            return HttpResponseRedirect(reverse('dashboard'))

        # storing the product id in the cache
        cache.set('product_id', pk, None)

        # storing the price of the product in the cache
        cache.set('price', product[0].price, None)

        # creating the context and rendering the html page where the particular
        # product will be displayed
        ctx = {
            'product': product[0], 'title': 'Dashboard', 'dashboard': 'active'
        }
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Post method for ProductDisplayView class."""
        pass


class ProfileView(TemplateView):
    """View for Profile page.

    The profile of the logged in user is displayed.
    """

    template_name = 'home/profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for ProfileView class."""
        # create the context and render the html page
        ctx = {'title': 'Profile'}
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Post method for ProfileView class."""
        pass


class EditProfileView(TemplateView):
    """View for Edit Profile page.

    The user can edit his profile from this view.
    """

    template_name = 'home/edit_profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for ProfileView class."""
        form = forms.EditProfileForm(request)
        return render(request, self.template_name, {
            'form': form, 'title': 'Edit Profile'})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Post method for EditProfileView class."""
        form = forms.EditProfileForm(request, request.POST, request.FILES)

        # if the form is valid and its attribute enctype="multipart/form-data"
        if form.is_valid() and form.is_multipart():
            try:
                # initialize 'data' with the cleaned data
                data = form.cleaned_data

                # intializing the 'upload_to' variable by a directory named
                # as the primary key of the user.
                upload_to = '/uploads/{0}/'.format(request.user.pk)

                # if request.FILES['image'] is empty, i.e no photo uploaded,
                # then intialize file_name to None
                try:
                    file_name = request.FILES['image']
                except:
                    file_name = None

                # initializing the 'image' variable with the directory name
                # and the file name
                image = '{0}{1}'.format(upload_to, file_name)

                # creating two dictionay to store the information
                # that will be later saved in the database
                data1, data2 = {}, {}
                data1 = {'first_name': data['first_name'],
                         'last_name': data['last_name']}
                data2 = {
                    'city': data['city'], 'address': data['address'],
                    'marital': data['marital'],
                    'date_of_birth': data['date_of_birth'],
                    'street': data['street'],
                    'phone': data['phone'], 'state': data['state'],
                    'extra_note': data['extra_note'],
                    'message': data['message'],
                    'other': data['other'], 'phonecall': data['phonecall'],
                    'mail': data['mail'], 'gender': data['gender'],
                    'user_id': request.user.pk, 'zip_code': data['zip_code']
                }

                # when the file_name is not None then upload
                try:
                    # saving image into the directory
                    save_file(file_name, upload_to)
                    # adding the image value(directory + filename) in the dict.
                    data2['image'] = image
                except Exception as e:
                    # pass
                    logger = logging.getLogger(constants.LOGGER)
                    logger.exception("No file to upload" + str(e))

                # updating auth_user and userdetail table
                User.objects.filter(pk=request.user.pk).update(**data1)
                UserDetail.objects.filter(
                    user_id=request.user.pk).update(**data2)

                # success message
                success_message = "Successfully saved."

                # creating the context
                ctx = ({
                    'form': form, 'title': 'Edit Profile',
                    'success_message': success_message})
                return render_to_response(
                    self.template_name, ctx,
                    context_instance=RequestContext(request))

            except Exception as e:
                # error message
                error_message = e
                # creating the context
                ctx = ({
                    'form': form, 'title': 'Edit Profile',
                    'error_message': error_message})
                return render_to_response(
                    self.template_name, ctx,
                    context_instance=RequestContext(request))
        else:
            # error message
            error_message = "Error...! "
            # creating the context
        ctx = ({
            'form': form, 'title': 'Edit Profile',
            'error_message': error_message})
        return render_to_response(
            self.template_name, ctx,
            context_instance=RequestContext(request))
        # return HttpResponse("something not right")


def save_file(f, upload_to):
    """Saving the photo in the directory."""
    file_name = f.name
    path = settings.MEDIA_ROOT + upload_to
    # create the directory if it doesnt exits
    if not os.path.exists(path):
        os.makedirs(path)
    destination = open(path + file_name, 'wb+')
    # write the file
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


class ScrapView(TemplateView):
    """View for the scraping page."""

    template_name = "home/scrap.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for the ScrapView class."""
        form = ScrapSearchForm()
        # creating a dictionary for the context
        ctx = {'form': form, 'title': 'Scrap page', 'scrap': 'active'}
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Post method for ScrapView class."""
        form = ScrapSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            search_item = data['search']

            # create an objec fo Scrap class
            obj = Scrap()
            product_list = None
            feedback = None
            # scrap the product based on user's choice of the website
            # 1 is for amazon and 2 is for flipkart
            if data['site_choice'] == '1':
                try:
                    product_list = obj.amazon(search_item)
                    # when no product is found,
                    # set the feedback with error message
                    if not product_list:
                        # no items found
                        feedback = True
                except:
                    # no items found
                    feedback = True
            else:
                try:
                    # import pdb
                    # pdb.set_trace()
                    product_list = obj.flipkart(search_item)
                    # when no product is found,
                    # set the feedback with error message
                    if not product_list:
                        # no items found
                        feedback = True
                except:
                    # no items found
                    feedback = True

        # creating the context
        ctx = {'result': product_list, 'scrap_result_error': feedback}
        html = render_to_string(
            'home/result.html', ctx,
            context_instance=RequestContext(request))
        json_data = json.dumps({'result': html})
        return HttpResponse(json_data, content_type='application/json')
