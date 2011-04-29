# coding=utf-8

from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext as _

from datetime import datetime, timedelta

from com_judge import ComJudge
from utils import are_equal


PROGRAMMING_LANGUAGES = (
    ('python', "Python 2.6"),
    ('pascal', "Pascal"),
    ('c', "C"),
    ('c++', "C++")
    #('java', _("Java")),
)

COMPETITION_STATUSES = (
    ('0', 'Standby'),
    ('1', 'In Progress'),
    ('2', 'In Evaluation'),
    ('3', 'Finish'),
)


class Competition(models.Model):
    """
    Competition model.

    # Create a competition
    >>> competition = Competition.objects.create(title="test", description="test")
    
    """
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    startTime = models.DateTimeField(null=True, blank=True)
    endTime = models.DateTimeField(null=True, blank=True)
    duration = models.BigIntegerField(null=True, blank=True)

    status = models.CharField(max_length=1,
                              choices=COMPETITION_STATUSES,
                              default=COMPETITION_STATUSES[0][0],
                              null=False)

    def start(self, duration):
        self.startTime = datetime.now()
        self.duration = duration
        self.endTime = self.startTime + timedelta(seconds=duration)
        self.transition_to_status(COMPETITION_STATUSES[1][0]) # In progress
        self.save(force_update=True)

    def stop(self):
        self.endTime = datetime.now()
        self.transition_to_status(COMPETITION_STATUSES[3][0])
        self.save(force_update=True)

    def reset(self):
        self.startTime = None
        self.endTime = None
        self.duration = None
        self.transition_to_status(COMPETITION_STATUSES[0][0])
        self.save(force_update=True)

    def transition_to_status(self, status):
        """
        Method to set status and fire events for the correspondent status.
        """
        if status == COMPETITION_STATUSES[0][0]: # Standby
            self.status = status
        elif status == COMPETITION_STATUSES[1][0]: # In Progress
            self.status = status
        elif status == COMPETITION_STATUSES[2][0]: # In Evaluation
            self.status = status
        elif status == COMPETITION_STATUSES[3][0]: # Finish
            self.status = status

    def get_remaining_time(self):
        """Return the remaining time of the competition in seconds"""
        if self.endTime >= datetime.now():
            delta = self.endTime - datetime.now()
            return delta.total_seconds()

    @models.permalink
    def problems(self):
        return ('competition.views.competition_problems', [str(self.id)])

    @models.permalink
    def solutions(self):
        return ('competition.views.competition_solutions', [str(self.id)])


    def __unicode__(self):
        return self.title


class Judge(User):
    """
    Judge model base class.
    """
    competition = models.ForeignKey(Competition)
    

class Organizer(User):
    """
    Organizer model.

    An organizer can add, modify and delete properties of the
    competition he belongs to.
    """
    competition = models.ForeignKey(Competition)


class Team(models.Model):
    """Team Model"""
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Participant(User):
    """
    Participant model
    """
    competition = models.ForeignKey(Competition)
    team = models.OneToOneField(Team)

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Problem(models.Model):
    """
    Problem model
    """
    competition = models.ManyToManyField(Competition, null=False, blank=False)

    title = models.CharField(_('Title'), max_length=255, unique=True)
    description = models.TextField(_('Description'))
    time_limit = models.IntegerField(_('Time limit'),
                                     help_text=_("Time limit in seconds"),
                                     default=5)
    input = models.TextField(_('Input'), blank=True, null=True)
    output = models.TextField(_('Output'), blank=True, null=True)

    sample_input = models.TextField(_('Sample Input'), null=True, blank=True)
    sample_output = models.TextField(_('Sample Output'), null=True, blank=True)
    sample_program = models.TextField(_('Sample Program'), null=True, blank=True)

    creation_time = models.DateTimeField(_('Creation Time'))

    @models.permalink
    def get_absolute_url(self):
        return ('competition.views.problem_detail', [str(self.id)])

    def __unicode__(self):
        return "Problem(" + self.title + ")"


class Solution(models.Model):
    """
    A solution is the submission of a participant to a problem.

    A solution can only be pointable result is set to 'Correct' and is accepted.
    """
    participant = models.ForeignKey(Participant)
    problem = models.ForeignKey(Problem)
    competition = models.ForeignKey(Competition)

    RESULT_CHOICE = (
        (0, _('Pending')),
        (1, _('Correct')),
        (2, _('Too late')), # Submitted after competition ended
        (3, _('Compile Error')),
        (4, _('Time limit exceeded')),
        (5, _('No Output')),
        (6, _('Wrong answer')),
        (7, _('Invalid submission'))
        #('8', _('Presentation error')),
    )

    source_code = models.TextField(_("Source code"))
    language = models.CharField(_("Programming language"), choices=PROGRAMMING_LANGUAGES, max_length=1)
    result = models.CharField(_("Result"), choices=RESULT_CHOICE, max_length=1, default=0)
    output = models.TextField(_("Output"), blank=True, null=True)
    error_message = models.TextField(_("Error message"), blank=True, null=True)

    accepted = models.BooleanField(_("Accepted"), default=False)

    submit_time = models.DateTimeField(_("Submit time"), auto_now_add=True)

    def compile_and_run(self):
        c = ComJudge(self.language, self.source_code, self.problem.output)
        c.run()

        status = c.get_status()
        return_code = status[0]
        output = status[1]
        error_message = status[2]

        # Result 'Invalid submission'
        ## The solution is an invalid submission if there is a previous solution which was accepted and
        ## which result is 'Correct'
        solutions = Solution.objects.filter(participant=self.participant, result=1, accepted=True)
        if solutions:
            for solution in solutions:
                if solution.result == 1 and solution.accepted == True:
                    self.result = 7

        # Result correct
        ## Result is correct if return_code == 0, there are no error messages,
        ## and output equals self.problem.output
        if return_code == 0 and are_equal(self.problem.output, output) and error_message in ("", None):
            self.result = 1 # Result correct
        # Result 'Compile Error'
        ## There is a compile error if returncode == 1 and there is an error message
        elif return_code == 1 and error_message:
            self.result = 3
        # Result 'Time limit exceeded'
        ## Time limit is exceeded when return code is 2
        elif return_code == 2:
            self.result = 4
        # Result 'No output'
        ## Happens when output is an empty string or None, but return_code is 0
        elif output in ("", None) and return_code == 0:
            self.result = 5
        # Result 'Wrong answer'
        ## Answer is wrong when output doesn't match the expected output
        elif not are_equal(self.problem.output, output):
            self.result = 6
        else:
            print return_code
            print output
            print error_message
            raise AssertionError("Should never reach this code!")
        # Result 'Too late'
        ## Result is 'Too late' if submit_time is greater than competition.endTime
        if self.competition.endTime:
            if self.submit_time > self.competition.endTime:
                self.result = 2

        self.output = status[1]
        self.error_message = status[2]

        self.save(force_update=True)

    def __unicode__(self):
        return "Solution #" + str(self.id)
