
"""
Inclusion tag for Organizer
"""

from django import template

register = template.Library()

@register.inclusion_tag('competition/templatetags/organizer/participant_list.html')
def participant_list(organizer):
    participants = organizer.competition.participant_set.all()

    return {"participants": participants}
