"""View for the home page."""
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class HomeView(TemplateView):
    """Class for the home page view."""

    template_name = 'home.html'
