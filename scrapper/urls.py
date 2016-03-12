"""Urls for the scrapper project."""
from django.conf.urls import include, url
from django.contrib import admin
# from apps import checkout
from apps.home import views
from apps.checkout.views import PaymentView
from apps.checkout.views import DeliveryDetailsView
from apps.checkout.views import SummaryView
# import apps

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', 'apps.usermanager.views.signup', name='signup'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {"next_page": "/"}, name='logout'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^login/$', 'apps.usermanager.views.app_login', name='app_login'),
    url(r'^activate/$', 'apps.usermanager.views.activate', name='activate'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/edit$', views.EditProfileView.as_view(),
        name='edit_profile'),
    url(r'^dashboard/scrap$', views.ScrapView.as_view(), name='scrap'),
    url(r'dashboard/filter/$', views.DashboardFilterView.as_view(),
        name='dashboard_filter'),
    url(r'^product/(?P<name>[-\w\d]+)/$', views.ProductDisplayView.as_view(), name="product_display"),
    url(r'^checkout/payment/$', PaymentView.as_view(), name='payment'),
    url(r'^checkout/address/$', DeliveryDetailsView.as_view(), name='delivery_address'),
    url(r'^checkout/summary/$', SummaryView.as_view(), name='summary'),
]
