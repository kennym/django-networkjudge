from django.conf.urls.defaults import patterns, include, url
from competition import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # Competition
    url(r'^competition/(\d+)/problems/$', views.competition_problems),
    url(r'^competition/(\d+)/solutions/$', views.competition_submissions),
    url(r'^competition/(\d+)/ranking/$', views.competition_ranking),

    # Problems
    url(r'^problem/(\d+)/$', views.problem_detail, name="problem-detail"),
    url(r'^problem/(\d+)/solution/submit/$', views.upload_submission, name="upload-submission"),

    # Judge
    url(r'^judge/problems/$', views.judge_problems),
    url(r'^judge/scoreboard/$', views.judge_scoreboard, name="judge-scoreboard"),
    url(r'^judge/submissions/$', views.judge_submissions),
    url(r'^judge/submission/(\d+)/judge/$', views.judge_submission_evaluate, name="submission-judge"),
    url(r'^judge/submission/(\d+)/verify/$', views.judge_verify_submission, name="verify-submission"),
    url(r'^judge/submission/(\d+)/ignore/$', views.judge_ignore_submission, name="ignore-submission"),

    # Authentication
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'competition/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'competition/index.html'}, name='logout'),
)