from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic import TemplateView
from apps.home import views as home_views

urlpatterns = [
    url(r'^$', home_views.HomeView.as_view(), name='home'),
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]
