from django.conf.urls import include, url
from django.contrib import admin
from apps.home import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', 'apps.usermanager.views.signup', name='signup'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {"next_page": "/"}, name='logout'),
    # function based view for dashboard
    # url(r'^dashboard/$', 'apps.home.views.dashboard', name='dashboard'),
    # class based view for dashboard
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    # url(r'^dashboard/', include('apps.home.urls')),
    url(r'^login/$', 'apps.usermanager.views.app_login', name='app_login'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    # url(r'^profile/', include('apps.home.urls')),
    url(r'^profile/edit$', views.EditProfileView.as_view(), name='edit_profile'),
    url(r'^dashboard/scrap$', views.ScrapView.as_view(), name='scrap'),
    url(r'^testing/$', views.TestingView.as_view(), name='testing'),
]
