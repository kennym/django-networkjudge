from django.conf.urls.defaults import patterns, include, url
from competition import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout_user, name='logout'),

    # Participants
    url(r'^participant/(\d+)/$', views.participant_view, name='participant-view'),
    url(r'^participant/(\d+)/upload_solution_for/(\d+)/$', views.upload_solution, name="participant-upload-solution"),
)
