
"""
Competition control panel
"""

from django import template

from competition.forms import StartCompetitionForm

register = template.Library()

@register.inclusion_tag('competition/templatetags/organizer/competition_cp.html')
def competition_cp(organizer):
    competition = organizer.competition
    if competition.status == 0:
        form = StartCompetitionForm()

    return {
        "competition": competition,
        "form": form
    }

    
