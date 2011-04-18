from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render_to_response,
    HttpResponseRedirect,
    Http404,
    RequestContext,
    redirect,
    get_object_or_404
)

from competition.forms import UploadSolutionForm
from competition.models import Participant, Solution, Problem

@login_required
def index(request):
    user = request.user
    if user.is_superuser:
        return redirect('/admin')
    print user.groups
    if user.groups == 1:
        return redirect(user.get_absolute_url())
    return render_to_response("competition/index.html", RequestContext(request))

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

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
                              RequestContext(request))

@login_required
def upload_solution(request, participant_id, problem_id):
    if request.method == "POST" and request.POST:
        form = UploadSolutionForm(request.POST, request.FILES)
        if form.is_valid():
            participant = get_object_or_404(Participant, pk=participant_id)
            problem = get_object_or_404(Problem, pk=problem_id)
            solution = Solution.objects.create(participant=participant, problem=problem, file=request.FILES['file'])
            solution.save()
            return HttpResponseRedirect(reverse('participant-view', args=[participant_id]))
        return participant_view(request, participant_id, {'form': form})
    else:
        raise Http404
