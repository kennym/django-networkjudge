from django.conf.urls.defaults import patterns, include, url
from competition import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # Competition
    url(r'^competition/(\d+)/problems/$', views.competition_problems),
    url(r'^competition/(\d+)/participant/(\d+)/$', views.participant_view, name='participant-view'),

    # Problems
    url(r'^competition/(\d+)/problem/(\d+)/submit/$', views.submit_solution, name="submit-solution"),

    # Authentication
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'competition/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'competition/index.html'}, name='logout'),

)