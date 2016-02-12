# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'add_another',
    url(r'^add/(?P<model_name>\w+)/?$', 'views.add_new_model', name='add_another'),
    url(r'^success/$', 'views.add_another_success', name='add_another_success'),
)


