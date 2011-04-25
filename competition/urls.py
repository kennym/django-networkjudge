from django.conf.urls.defaults import patterns, include, url
from competition import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # Competition
    url(r'^competition/(\d+)/problems/$', views.competition_problems),
    url(r'^competition/(\d+)/solutions/$', views.competition_solutions),
    url(r'^competition/(\d+)/participant/(\d+)/$', views.participant_view, name='participant-view'),

    # Problems
    url(r'^problem/(\d+)/$', views.problem_detail, name="problem-detail"),
    url(r'^problem/(\d+)/submit/$', views.submit_solution, name="submit-solution"),

    # Solutions
    url(r'^judge/(\d+)/solution/(\d+)/evaluate/$', views.solution_evaluate, name="solution-evaluate"),

    # Authentication
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'competition/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'competition/index.html'}, name='logout'),
)