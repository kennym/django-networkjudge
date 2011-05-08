from django import template
from competition.models import Submission, Participant, Competition

register = template.Library()

@register.inclusion_tag('competition/templatetags/show_overview.html')
def show_overview(participant):
    problems = participant.competition.problem_set.filter(competition=participant.competition).order_by('id')

    competition = participant.competition
    participants = competition.participant_set.all().order_by('score')

    # Find rank of participant
    rank = 0
    for r, part in enumerate(participants):
        if part == participant:
            rank = r + 1

    # Create a new list with dictionaries for each problem which looks like this:
    # problems = [{
    #   "solved": True,
    #   "submissions": int()
    #   "problem": Problem
    #
    problem_meta = []
    for problem in problems:
        new_dict = {"solved": False,
                    "submissions": 0,
                    "problem": None}
        for submission in problem.submission_set.filter(participant=participant):
            # Add a submission
            new_dict["submissions"] += 1
            if submission.result_correct():
                new_dict["solved"] = True
            # Add problem to dict
            new_dict["problem"] = problem
        problem_meta.append(new_dict)

    context = {
        "problems": problem_meta,
        "participant": participant,
        "rank": rank
    }

    return context

