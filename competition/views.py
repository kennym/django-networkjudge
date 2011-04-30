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
    EvaluateSubmissionForm
)
from competition.models import (
    Competition,
    Judge,
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
            #organizer = user.organizer or None
            if participant:
                competition = participant.competition
            if judge:
                competition = judge.competition
        except Participant.DoesNotExist, e:
            pass
        except Judge.DoesNotExist, e:
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
def problem_detail(request, id):
    problem = get_object_or_404(Problem, pk=id)
    context = {
        "problem": problem
    }
    return render_to_response("competition/problem/detail.html",
                              context,
                              context_instance=RequestContext(request))

@login_required
def participant_view(request, id, extra_context=None):
    participant = get_object_or_404(Participant, pk=id)
    competition = participant.competition
    team = participant.team
    problems = competition.problem_set.all()
    context = {
        "participant": participant,
        "competition": competition,
        "team": team,
        "problems": problems,
        "form": UploadSubmissionForm()
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response("competition/participant/index.html",
                              context,
                              context_instance=RequestContext(request))


@login_required
def upload_submission(request, problem_id):
    if request.method == "POST" and request.POST:
        form = UploadSubmissionForm(request.POST)
        if form.is_valid():
            participant = get_object_or_404(Participant, pk=request.user.id)

            submission = form.save(commit=False)
            submission.participant = participant
            problem = get_object_or_404(Problem, pk=problem_id)
            submission.competition = participant.competition
            submission.problem = problem
            submission.save()
            submission.compile_and_run()
            return render_to_response("competition/submission/submit.html",
                                      {'submission': submission},
                                      context_instance=RequestContext(request))
        return render_to_response("competition/submission/submit.html",
                                  {'form': form},
                                  context_instance=RequestContext(request))
    else:
        problem = get_object_or_404(Problem, pk=problem_id)
        participant = get_object_or_404(Participant, pk=request.user.id)
        submission = None
        for sol in participant.submission_set.all():
            if sol.problem == problem:
                submission = sol
        context = {
            "form": UploadSubmissionForm(),
            "competition": get_object_or_404(Competition, pk=participant.competition.id),
            "problem": problem,
            "submission": submission
        }
        return render_to_response("competition/submission/submit.html",
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
    form = EvaluateSubmissionForm(instance=submission)

    context = {
        "submission": submission,
        "form": form
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

