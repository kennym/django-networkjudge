from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import (
    render_to_response,
    RequestContext,
    redirect,
    get_object_or_404,
    Http404
)

from competition.forms import (
    UploadSubmissionForm,
    IgnoreSubmissionForm,
    VerifySubmissionForm
)
from competition.models import (
    Competition,
    Judge,
    Organizer,
    Participant,
    Problem,
    Submission
)


def index(request):
    user = request.user
    if user.is_authenticated():
        if user.is_superuser:
            return redirect('/admin')

        judge = None
        participant = None
        competition = None
        try:
            participant = user.participant or None
            judge = user.judge or None
            organizer = user.organizer or None
            if participant:
                competition = participant.competition
            if judge:
                competition = judge.competition
            if organizer:
                competition = organizer.competition
        except Participant.DoesNotExist, e:
            pass
        except Judge.DoesNotExist, e:
            pass
        except Organizer.DoesNotExist, e:
            pass
        except Exception, e:
            raise

        context = {
            "competition": competition
        }
    else:
        competitions = Competition.objects.all()
        context = {
            "competitions": competitions
        }
    return render_to_response("competition/index.html", context, context_instance=RequestContext(request))

@login_required
def competition_problems(request, id):
    competition = get_object_or_404(Competition, pk=id)
    problems = competition.problem_set.all()

    context = {
        'competition': competition,
        'problems': problems
    }

    return render_to_response("competition/problem/list.html", context, context_instance=RequestContext(request))


@login_required
def competition_submissions(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    submissions = competition.submission_set.all()

    context = {
        "objects": submissions
    }

    return render_to_response("competition/submission/list.html",
                              context,
                              RequestContext(request))

@login_required
def competition_ranking(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    return render_to_response("competition/ranking.html",
                              {"competition": competition},
                              RequestContext(request))


@login_required
def problem_detail(request, id):
    problem = get_object_or_404(Problem, pk=id)
    context = {
        "problem": problem
    }
    return render_to_response("competition/problem/detail.html",
                              context,
                              context_instance=RequestContext(request))

@login_required
def upload_submission(request, problem_id):
    if request.method == "POST" and request.POST:
        form = UploadSubmissionForm(request.POST)
        problem = get_object_or_404(Problem, pk=problem_id)
        if form.is_valid():
            participant = get_object_or_404(Participant, pk=request.user.id)

            submission = form.save(commit=False)
            submission.participant = participant
            problem = get_object_or_404(Problem, pk=problem_id)
            submission.competition = participant.competition
            submission.problem = problem
            submission.save()
            submission.compile_and_run()
            return redirect(index)
        return render_to_response("competition/submission/submit.html",
                                  {
                                      'form': form,
                                      'problem': problem
                                  },
                                  context_instance=RequestContext(request))
    else:
        problem = get_object_or_404(Problem, pk=problem_id)
        participant = get_object_or_404(Participant, pk=request.user.id)
        submissions = Submission.objects.filter(participant=participant, problem=problem)

        context = {
            "form": UploadSubmissionForm(),
            "competition": get_object_or_404(Competition, pk=participant.competition.id),
            "problem": problem,
            "submissions": submissions
        }
        return render_to_response("competition/submission/submit.html",
                                  context,
                                  context_instance=RequestContext(request))

#######################################################################
# Participant
######################################################################

@login_required
def participant_scoreboard(request):
    participant = request.user.participant
    participants = Participant.objects.all().order_by('score')

    context = {
        "participants": participants,
        "participant": participant
    }

    return render_to_response("competition/participant/scoreboard.html",
                              context,
                              context_instance=RequestContext(request))


@login_required
def judge_submission_evaluate(request, submission_id):
    judge = None
    try:
        judge = request.user.judge
    except:
        raise Http404

    submission = get_object_or_404(Submission, pk=submission_id)
    verify_form = VerifySubmissionForm(instance=submission)
    ignore_form = IgnoreSubmissionForm(instance=submission)

    context = {
        "submission": submission,
        "verify_form": verify_form,
        "ignore_form": ignore_form
    }

    return render_to_response("competition/judge/evaluate.html",
                              context,
                              context_instance=RequestContext(request))

@login_required
def judge_submissions(request):
    judge = None
    try:
        judge = request.user.judge
    except:
        raise Http404

    submissions = judge.competition.submission_set.all()

    context = {
        "submissions": submissions
    }

    return render_to_response("competition/judge/submissions.html",
                              context,
                              context_instance=RequestContext(request))

@login_required
def judge_problems(request):
    judge = None
    try:
        judge = request.user.judge
    except:
        raise Http404

    problems = judge.competition.problem_set.all()

    context = {
        "problems": problems
    }

    return render_to_response("competition/judge/problems.html",
                              context,
                              context_instance=RequestContext(request))

@login_required
def judge_verify_submission(request, submission_id):
    judge = None
    try:
        judge = request.user.judge
    except:
        raise Http404

    if request.method == "POST" and request.POST:
        submission = get_object_or_404(Submission, pk=submission_id)
        form = VerifySubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.claimed_by = judge
            submission.save()
            return judge_submissions(request)
        else:
            return judge_submission_evaluate(request, submission_id)
    else:
        return Http404

@login_required
def judge_ignore_submission(request, submission_id):
    judge = None
    try:
        judge = request.user.judge
    except:
        raise Http404

    if request.method == "POST" and request.POST:
        submission = get_object_or_404(Submission, pk=submission_id)
        form = IgnoreSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.save()
            return judge_submissions(request)
        else:
            return judge_submission_evaluate(request, submission_id)
    else:
        return Http404

@login_required
def judge_scoreboard(request):
    participants = Participant.objects.all().order_by('score')

    context = {
        "participants": participants
    }
    return render_to_response("competition/judge/scoreboard.html",
                              context,
                              context_instance=RequestContext(request))

