__author__ = 'Sam'

from django.conf.urls import patterns, url

from frc_scout import views

urlpatterns = patterns(
    '',

    # Views dealing with session stuff stored in session_views.py
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^create/$', views.create_account, name='create_account'),

    # JSON calls
    url(r'^json/team_exists/$', views.check_if_team_exists, name='check_if_team_exists'),
    url(r'^json/username_exists/$', views.check_if_username_exists, name='check_if_username_exists'),

)