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
    url(r'search/circles', 'matches.views.search_circles_form', name='search_circles_form'),
    url(r'add_to_circle_form', 'matches.views.add_to_circle_form', name='add_to_circle_form'),
    url(r'advocate/add_circle', 'matches.views.add_circle', name='add_circle'),
    url(r'advocate/show_circle', 'matches.views.show_circle_list', name='show_circle'),
    url(r'^advocate$', 'matches.views.advocate_homepage', name='advocate_homepage'),


    url(r'^single/create', views.SingleCreate.as_view(), name='single_create'),
     url(r'^single/edit/(?P<pk>\d+)$', views.SingleUpdate.as_view(), name='single_edit'),
    # url(r'^single/edit/(?P<pk>\d+)$', 'matches.views.update_single', name='single_edit'),
    url(r'^search/single', 'matches.views.single_search_form', name='single_search_form'),
    url(r'^show_profile/(?P<pk>\d+)$', 'matches.views.display_single_profile', name='single_profile'),
    url(r'^search_single', 'matches.views.search_single', name='search_single'),
    url(r'email/single_profile/(?P<pk>\d+)$', 'matches.views.edit_single_profile', name='email_single_profile'),
    url(r'email/send', 'matches.views.send_email', name='send_email'),

    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
