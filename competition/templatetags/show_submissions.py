from django import template
from competition.models import Submission

register = template.Library()

@register.inclusion_tag('competition/templatetags/show_submissions.html')
def show_submissions(participant):
    """
    Return all submissions from the given Participant

    @param participant Instance of :model:`competition.Participant`
    """
    submissions = Submission.objects.filter(participant=participant).order_by('-submit_time')

    return {"submissions": submissions}

