"""View for the home page."""
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.usermanager import forms
from django.contrib.auth.models import User
from apps.usermanager.models import UserDetail
from django.http import HttpResponse
from django.conf import settings
import os
from apps.home.scrap import Scrap
from apps.home.forms import ScrapSearchForm
from apps.home.forms import DashboardSearchForm
from apps.home.models import Product
from django.db.models import Q


class HomeView(TemplateView):
    """Class for the home page view."""

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        """Get method for HomeView class."""
        ctx = {'title': 'Home', 'home': 'active'}
        return render(request, self.template_name, ctx)


class DashboardView(TemplateView):
    """Class for the dashboard view."""

    template_name = 'dashboard.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for DashboardView class."""
        form = DashboardSearchForm(request.GET)
        products = []
        result_error = ""
        if form.is_valid():
            data = form.cleaned_data
            search_item = data['search']
            products = Product.objects.filter(
                Q(name__icontains=search_item) |
                Q(price__icontains=search_item) |
                Q(site_reference__icontains=search_item) |
                Q(product_type__icontains=search_item) |
                Q(description__icontains=search_item)
            )
            if not products:
                result_error = "No result found, please scape this item"
        ctx = {
            'title': 'Dashboard', 'dashboard': 'active', 'form': form,
            'result': products, 'result_error': result_error
        }
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pass


class ProfileView(TemplateView):
    """View for Profile page."""

    template_name = 'profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for ProfileView class."""
        ctx = {'title': 'Profile'}
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pass


class EditProfileView(TemplateView):
    """View for Edit Profile page."""

    template_name = 'edit_profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Get method for ProfileView class."""
        form = forms.EditProfileForm(request)
        return render(request, self.template_name, {'form': form, 'title': 'Edit Profile'})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = forms.EditProfileForm(request, request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            try:
                data = request.POST.copy()
                # handling the unchecked checkbox
                # and radio button values
                try:
                    mail = data['mail']
                except:
                    mail = None
                try:
                    message = data['message']
                except:
                    message = None
                try:
                    phonecall = data['phonecall']
                except:
                    phonecall = None
                try:
                    other = data['other']
                except:
                    other = None
                try:
                    gender = data['gender']
                except:
                    gender = None
                # handling the date field and number value
                if data['date_of_birth'] in ['', ' ', None]:
                    data['date_of_birth'] = None
                if data['phone'] in ['', ' ', None]:
                    data['phone'] = None
                # uploading the image by creating a directory named
                # as the primary key of the user.
                upload_to = '/uploads/{0}/'.format(request.user.pk)
                # if request.FILES['image'] is empty intialize file_name to None
                try:
                    file_name = request.FILES['image']
                except:
                    file_name = None
                image = '{0}{1}'.format(upload_to, file_name)
                data1, data2 = {}, {}
                data1 = {'first_name': data['first_name'],
                         'last_name': data['last_name']}
                data2 = {
                    'city': data['city'], 'address': data['address'],
                    'marital': data['marital'], 'date_of_birth': data['date_of_birth'],
                    'street': data['street'],
                    'phone': data['phone'], 'state': data['state'],
                    'extra_note': data['extra_note'], 'message': message,
                    'other': other, 'phonecall': phonecall,
                    'mail': mail, 'gender': gender,
                    'user_id': request.user.pk, 'zip_code': data['zip_code']
                }
                # when the file_name is not None then upload
                if file_name not in [None]:
                    # saving image into the directory
                    save_file(file_name, upload_to)
                    # adding the image value(directory + filename) in the dict.
                    data2['image'] = image
                else:
                    print ('no image hence file not uploaded')
                # handling the checkbox values before storing in database
                if data2['mail'] == 'on':
                    data2['mail'] = True
                else:
                    data2['mail'] = False
                if data2['message'] == 'on':
                    data2['message'] = True
                else:
                    data2['message'] = False

                if data2['phonecall'] == 'on':
                    data2['phonecall'] = True
                else:
                    data2['phonecall'] = False

                if data2['other'] == 'on':
                    data2['other'] = True
                else:
                    data2['other'] = False
                User.objects.filter(pk=request.user.pk).update(**data1)
                UserDetail.objects.filter(user_id=request.user.pk).update(**data2)
                # issue3 phone range is short
                print('success')
                return HttpResponse("success")

            except Exception as e:
                print(e)
        else:
            return HttpResponse("error")
            print (form.errors)
        return HttpResponse("something not right")


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
    """View for the scraping page"""
    template_name = "scrap.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = ScrapSearchForm()
        ctx = {'form': form, 'title': 'Scrap page', 'scrap': 'active'}
        return render(request, self.template_name, ctx)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = ScrapSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            search_item = data['search']
            obj = Scrap()
            product_list = obj.amazon(search_item) if data['site'] == '1' else obj.flipkart(search_item)
        ctx = {'result': product_list, 'form': form}
        return render(request, self.template_name, ctx)
        # return HttpResponse("result shown")



class TestingView(TemplateView):
    """Testing html pages"""

    template_name = 'hello.html'
    def get(self, request, *args, **kwargs):
        ctx = {'title': 'testing', 'home': 'active'}
        return render(request, self.template_name, ctx)
