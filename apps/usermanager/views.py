"""Views for usermanager app.

Signup, login and acitivation views.
"""
from apps.usermanager import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.models import make_password
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from apps.usermanager.models import UserDetail
from apps.usermanager.models import UserActivation
from apps import constants
from django.core.mail import send_mail
from django.conf import settings
import hashlib
import random


def signup(request):
    """View for Signup."""
    if request.user.pk:
        print (request.user)
        return HttpResponseRedirect(reverse('dashboard'))
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['confirm_password'] == data['password']:
                data.pop('confirm_password')
                password = data['password']
                # encrypting the password before storing in database
                data['password'] = make_password(
                    data['password'], salt="scrapper")

                # setting the is_active field to false by defautl
                data['is_active'] = False

                # creating the user
                user = User.objects.create(**data)
                # creating a record in UserDetail table,
                # with the current registered user id.
                data1 = {'user_id': user.pk}
                UserDetail.objects.create(**data1)

                # generating an unique acitivation key
                activation_key = generate_activation_key(data['email'])
                data2 = {'user_id': user.pk, 'activation_key': activation_key}

                # creating a record in the UserActivation table
                UserActivation.objects.create(**data2)
            else:
                user = None
                messages.error(request, 'Password did not match.')
                ctx = ({'form': form, 'title': 'Signup', 'register': 'active', 'nav_dashboard': 'nav-dashboard'})
                return render_to_response(
                    'signup.html', ctx,
                    context_instance=RequestContext(request))

            ctx = ({'message': ''})
            if user:
                # sending activation email
                try:
                    send_activation_mail(
                        user.username, data['email'], activation_key)

                    # displaying message to the user to activate his accont
                    message = 'An acitvation link has been sent to your email id.\
                    Please activate.'

                    # creating the context
                    ctx = ({'message_success': message, 'title': 'Signup'})

                    return render_to_response(
                        'signup.html', ctx,
                        context_instance=RequestContext(request))
                except Exception as e:
                    # displaying error message on email sending failure.
                    messages.error(request, 'Email sending failed.' + e)

                    # creating the context
                    ctx = ({'form': form, 'title': 'Signup', 'register': 'active', 'nav_dashboard': 'nav-dashboard'})
                    return render_to_response(
                        'signup.html', ctx,
                        context_instance=RequestContext(request))
            else:
                pass
    elif request.method == 'GET':
        form = forms.SignUpForm()
    ctx = ({'form': form, 'title': 'Signup', 'register': 'active', 'nav_dashboard': 'nav-dashboard'})
    return render_to_response(
        'signup.html', ctx, context_instance=RequestContext(request)
    )


def generate_activation_key(email):
    """Generating an unique acitivation key."""
    salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
    activation_key = hashlib.sha1(
        str(salt + email).encode('utf-8')).hexdigest()
    return activation_key


def send_activation_mail(username, receiver_email, activation_key):
    """Sending an acitvation mail to the registered user."""
    subject = "Acitvation Email - Scrapper.com"
    # message to be sent
    message = "Activation email"
    html_message = "Click <a href='{0}?id={1}'>here</a> \
    to activate your account".format(constants.ACTIVATION_URL, activation_key)
    from_email = settings.EMAIL_HOST_USER
    to_email = [receiver_email]

    # sending email
    send_mail(
        subject, message, from_email, to_email,
        fail_silently=False, html_message=html_message)


def activate(request):
    """Activating the user.

    Updating the is_active field in the auth_user table from False to True.
    """
    if request.method == 'GET':
        data = request.GET.copy()
        print (data['id'])
        key = data['id']
        ua = UserActivation.objects.get(activation_key=key)
        print (ua.user_id)
        data = {'is_active': True}
        User.objects.filter(pk=ua.user_id).update(**data)
    ctx = {'title': 'Activation'}
    return render_to_response(
        'activate.html', ctx, context_instance=RequestContext(request)
    )


def app_login(request):
    """View for login."""
    form = forms.LoginForm()
    # nav-dashboard is the css class for custom navbar in login page
    ctx = ({'form': form, 'nav_dashboard': 'nav-dashboard'})
    # if the user is logged in redirect him to the dashboard page
    if request.user.pk:
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            # initializing the data varialbe with cleaned data
            data = form.cleaned_data

            # authenticating the username and password
            auth_user = authenticate(
                username=data['username'], password=data['password']
            )
            # if the user is authenticated,
            # check whether his account is active or not
            if auth_user:
                # if the account is acitve redirect to dashboard page
                if auth_user.is_active:
                    login(request, auth_user)
                    return HttpResponseRedirect(reverse('dashboard'))
                # otherwise display error meassage to activate his account
                else:
                    messages.error(request, 'Please activate your account')
                ctx = ({'form': form, 'nav_dashboard': 'nav-dashboard', 'login': 'active'})
                return render_to_response(
                    'login.html', ctx,
                    context_instance=RequestContext(request))
            # if the user is not an authenticated user display error message
            else:
                messages.error(request, 'Wrong username or password.')
                ctx = ({'form': form, 'nav_dashboard': 'nav-dashboard', 'login': 'active'})
                return render_to_response(
                    'login.html', ctx,
                    context_instance=RequestContext(request))

    elif request.method == 'GET':
        form = forms.LoginForm()
    ctx = ({'form': form, 'title': 'Login', 'nav_dashboard': 'nav-dashboard', 'login': 'active'})
    return render_to_response(
        'login.html', ctx, context_instance=RequestContext(request)
    )
