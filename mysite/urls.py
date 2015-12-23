from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from matches import views

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),

    url(r'^$', 'matches.views.home', name='home'),
    url(r'^login', 'matches.views.login', name='login'),
    url(r'^logout', 'matches.views.logout', name='logout'),

    url(r'^advocate/signup', 'matches.views.advocate_signup', name='advocate_signup'),
    url(r'^advocate/edit/(?P<pk>\d+)$', 'matches.views.update_advocate', name='advocate_edit'),
    url(r'add_to_circle_form', 'matches.views.add_to_circle_form', name='add_to_circle_form'),
    url(r'advocate/add_circle', 'matches.views.add_circle', name='add_circle'),
    url(r'^advocate$', 'matches.views.advocate_homepage', name='advocate_homepage'),
    url(r'^advocate_contact/(?P<pk>\d+)$', 'matches.views.display_advocate_contact_info', name='advocate_contact_info'),


    url(r'^single/create', views.SingleCreate.as_view(), name='single_create'),
     url(r'^single/edit/(?P<pk>\d+)$', views.SingleUpdate.as_view(), name='single_edit'),
    # url(r'^single/edit/(?P<pk>\d+)$', 'matches.views.update_single', name='single_edit'),
    url(r'^show_profile/(?P<pk>\d+)$', 'matches.views.display_single_profile', name='single_profile'),
    url(r'^single/change_status/(?P<pk>\d+)$', 'matches.views.change_single_status_form', name='change_single_status'),


    url(r'^search/single', 'matches.views.single_search_form', name='single_search_form'),
    url(r'get_search_results', 'matches.views.get_search_results', name='get_search_results'),

    url(r'search_results/by_advocate', 'matches.views.search_results_by_advocate', name='search_results_by_advocate'),
    url(r'search_results/by_circle', 'matches.views.search_results_by_circle', name='search_results_by_circle'),
    url(r'^search_results/single', 'matches.views.search_results_single', name='search_results_single'),


    url(r'email/single_profile/(?P<pk>\d+)$', 'matches.views.email_single_profile', name='email_single_profile'),
    url(r'email/request_resume/(?P<pk>\d+)$', 'matches.views.email_request_resume', name='request_resume'),
    url(r'email/send', 'matches.views.send_email', name='send_email'),

    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
