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
from com_judge import ComJudge


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
        "form": UploadSolutionForm()
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response("competition/participant/index.html",
                              context,
                              context_instance=RequestContext(request))


@login_required
def submit_solution(request, problem_id):
    if request.method == "POST" and request.POST:
        form = UploadSolutionForm(request.POST)
        if form.is_valid():
            participant = get_object_or_404(Participant, pk=request.user.id)

            # Check if participant has already submitted a solution
            queryset = Solution.objects.filter(participant__exact=participant.id)
            if queryset.exists():
                messages.add_message(request, messages.ERROR, _("You already submitted a solution."))
                solution = queryset.all()[0]
            else:

                solution = form.save(commit=False)
                compiler = None
                if solution.language == "A":
                    compiler = "python"
                elif solution.language == "B":
                    compiler = "javac"

                c = ComJudge(compiler, solution.source_code)
                c.run()
                status = c.get_status()

                solution.result = status[0]
                solution.error_message = status[2] or None
                solution.participant = participant
                problem = get_object_or_404(Problem, pk=problem_id)
                solution.problem = problem
                solution.save()
            return render_to_response("competition/solution/submit.html",
                                      {'solution': solution},
                                      context_instance=RequestContext(request))
        return render_to_response("competition/solution/submit.html",
                                  {'form': form},
                                  context_instance=RequestContext(request))
    else:
        problem = get_object_or_404(Problem, pk=problem_id)
        participant = get_object_or_404(Participant, pk=request.user.id)
        solution = None
        # TODO: Use solutions instead of solution
        for sol in participant.solution_set.all():
            if sol.problem == problem:
                solution = sol
        context = {
            "form": UploadSolutionForm(),
            "competition": get_object_or_404(Competition, pk=participant.competition.id),
            "problem": problem,
            "solution": solution
        }
        return render_to_response("competition/solution/submit.html",
                                  context,
                                  context_instance=RequestContext(request))
