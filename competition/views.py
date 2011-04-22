from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import (
    render_to_response,
    HttpResponseRedirect,
    Http404,
    RequestContext,
    redirect,
    get_object_or_404
)

from competition.forms import UploadSolutionForm
from competition.models import Participant, Solution, Problem, Competition


def index(request):
    user = request.user
    if user.is_authenticated():
        if user.is_superuser:
            return redirect('/admin')

        try:
            participant = user.participant or None
            #judge = user.judge or None
            #organizer = user.organizer or None
            competition = participant.competition
        except Exception, e:
            raise e

        context = {
            "participant": participant,
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

    return render_to_response("competition/problems.html", context, context_instance=RequestContext(request))


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
        "form": UploadSolutionForm()
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response("competition/participant/index.html",
                              context,
                              context_instance=RequestContext(request))


@login_required
def submit_solution(request, competition_id, problem_id):
    if request.method == "POST" and request.POST:
        form = UploadSolutionForm(request.POST)
        if form.is_valid():
            participant = get_object_or_404(Participant, pk=request.user.id)
            # Check if participant has already submitted a solution
            queryset = Solution.objects.filter(participant__exact=participant.id)
            if queryset.exists():
                messages.add_message(request, messages.ERROR, _("You already submitted a solution."))
                solution = queryset.all()[0]
                return render_to_response("competition/solution/submit.html",
                                          {'solution': solution},
                                          context_instance=RequestContext(request))
            else:
                problem = get_object_or_404(Problem, pk=problem_id)

                solution = form.save(commit=False)
                solution.participant = participant
                solution.problem = problem
                solution.save()
                return render_to_response("competition/solution/submit.html",
                                          {'solution': solution},
                                          context_instance=RequestContext(request))
        return render_to_response("competition/solution/submit.html",
                                  {'form': form},
                                  context_instance=RequestContext(request))
    else:
        context = {
            "form": UploadSolutionForm(),
            "competition": get_object_or_404(Competition, pk=competition_id),
            "problem": get_object_or_404(Problem, pk=problem_id)
        }
        return render_to_response("competition/solution/submit.html",
                                  context,
                                  context_instance=RequestContext(request))
