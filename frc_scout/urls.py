__author__ = 'Sam'

from django.conf.urls import patterns, url

from frc_scout import views

urlpatterns = patterns(
    '',
    url(r'^$', views.login, name='login')
)