from django import template
from competition.models import Submission, Participant, Judge

register = template.Library()

@register.inclusion_tag('competition/templatetags/show_submissions.html')
def show_submissions(user):
    """
    Return all submissions from the given user
    """
    submissions = None
    try:
        if user.participant:
            submissions = Submission.objects.filter(participant=participant).order_by('-submit_time')
        if user.judge:
            submissions = Submission.objects.all().order_by('-submit_time')
    except Participant.DoesNotExist, e:
        pass
    except Judge.DoesNotExist, e:
        pass

    return {"submissions": submissions,
            "user": user}

