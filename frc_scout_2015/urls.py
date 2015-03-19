from django.conf.urls import patterns, include, url
from django.contrib import admin

import debug_toolbar

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'frc_scout_2015.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('frc_scout.urls', namespace='frc_scout')),
	url(r'^__debug__/', include(debug_toolbar.urls)),

	)
