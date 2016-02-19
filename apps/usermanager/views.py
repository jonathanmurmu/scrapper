from django.shortcuts import render
from apps.usermanager import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.models import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from apps.usermanager.models import UserDetail


# Create your views here.

def signup(request):
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
                data['password'] = make_password(data['password'], salt="scrapper")
                user = User.objects.create(**data)
                # creating a record in UserDetail table,
                # with the current registered user id.
                UserDetail.objects.create(user_id=user.pk)
            else:
                user = None
                messages.error(request, 'Password did not match.')
                ctx = ({'form': form})
                return render_to_response('signup.html', ctx, context_instance=RequestContext(request))
            if user:
                auth_user = authenticate(
                    username=data['username'], password=password
                )
                if auth_user:
                    login(request, auth_user)
                    return HttpResponseRedirect(reverse('dashboard'))
            else:
                pass
    elif request.method == 'GET':
        form = forms.SignUpForm()
    ctx = ({'form': form})
    return render_to_response(
        'signup.html', ctx, context_instance=RequestContext(request)
    )


def app_login(request):
    form = forms.LoginForm()
    ctx = ({'form': form})
    if request.user.pk:
        return HttpResponseRedirect(reverse('dashboard'))
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            auth_user = authenticate(
                username=data['username'], password=data['password']
            )
            if auth_user:
                login(request, auth_user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                messages.error(request, 'Wrong username or password.')
                ctx = ({'form': form})
                return render_to_response('login.html', ctx, context_instance=RequestContext(request))

    elif request.method == 'GET':
        form = forms.LoginForm()
    ctx = ({'form': form})
    return render_to_response(
        'login.html', ctx, context_instance=RequestContext(request)
    )
