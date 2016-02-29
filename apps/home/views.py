"""View for the home page."""
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
from apps.home.models import Product
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
import logging
from apps import constants


class HomeView(TemplateView):
    """Class for the home page view."""

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        """Get method for HomeView class."""
        ctx = {'title': 'Home', 'home': 'active'}
        return render(request, self.template_name, ctx)


class DashboardView(TemplateView):
    """Class for the dashboard view.

    Allows user to search for the product,
     and display the result in the front end.
    The results are fetched from the database.
    """

    template_name = 'dashboard.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for DashboardView class."""
        products = []
        result_error = ""
        if request.GET:
            form = DashboardSearchForm(request.GET)
            # to display the error message
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
                # when no resuts are found set the result error variable
                if not products:
                    result_error = "No result found error."
        else:
            form = DashboardSearchForm()
        # create a dictionary for the context
        ctx = {
            'title': 'Dashboard', 'dashboard': 'active', 'form': form,
            'result': products, 'result_error': result_error
        }
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Post method for DashboardView class."""
        pass


class ProfileView(TemplateView):
    """View for Profile page.

    The profile of the logged in user is displayed.
    """

    template_name = 'profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for ProfileView class."""
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

    template_name = 'edit_profile.html'

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

                # if request.FILES['image'] is empty
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
                    'edit_profile.html', ctx,
                    context_instance=RequestContext(request))

            except Exception as e:
                # error message
                error_message = e
                # creating the context
                ctx = ({
                    'form': form, 'title': 'Edit Profile',
                    'error_message': error_message})
                return render_to_response(
                    'edit_profile.html', ctx,
                    context_instance=RequestContext(request))
        else:
            # error message
            error_message = "Error...! "
            # creating the context
        ctx = ({
            'form': form, 'title': 'Edit Profile',
            'error_message': error_message})
        return render_to_response(
            'edit_profile.html', ctx,
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

    template_name = "scrap.html"

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
            if data['site_choice'] == '1':
                try:
                    product_list = obj.amazon(search_item)
                    # when no product is found,
                    # set the feedback with error message
                    if not product_list:
                        feedback = "Search item not found"
                except:
                    feedback = " Search item not found"
            else:
                try:
                    product_list = obj.flipkart(search_item)
                    # when no product is found,
                    # set the feedback with error message
                    if not product_list:
                        feedback = "Search item not found"
                except:
                    feedback = " Search item not found"

        # creating a dictionary for the context
        ctx = {
            'result': product_list, 'form': form, 'scrap': 'active',
            'title': 'Scrap page', 'feedback': feedback
        }
        return render(request, self.template_name, ctx)
        # return HttpResponse("result shown")


class TestingView(TemplateView):
    """Testing html pages.

    Delete this class, its only for experimenting.
    """

    template_name = 'hello.html'

    def get(self, request, *args, **kwargs):
        """Get method to TestingView class."""
        ctx = {'title': 'testing', 'home': 'active'}
        return render(request, self.template_name, ctx)
