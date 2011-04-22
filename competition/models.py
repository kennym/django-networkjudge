# coding=utf-8

from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext as _

from datetime import datetime, timedelta


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

    An organizer can add, modify and delete properties of the competition he belongs
     to.

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
    input = models.TextField(_('Input'), null=True, blank=True)
    output = models.TextField(_('Output'), null=True, blank=True)
    sample_output = models.TextField(_('Sample Output'), null=True, blank=True)
    sample_input = models.TextField(_('Sample Input'), null=True, blank=True)
    sample_program = models.TextField(_('Sample Program'), null=True, blank=True)

    creation_time = models.DateTimeField(_('Creation Time'))

    def __unicode__(self):
        return "Problem(" + self.title + ")"


class Solution(models.Model):
    """
    A solution is the submission of a participant to a problem.
    """
    participant = models.OneToOneField(Participant)
    problem = models.ForeignKey(Problem)

    PROGRAMMING_LANGUAGES = {
        ('A', _("Python 2.6")),
        ('B', _("Java"))
    }
    RESULT_CHOICE = (
        ('A',_('Accepted')),
        ('C',_('Compile Error')),
        ('E',_('System Error(FILE)')),
        ('F',_('Restrict Function')),
        ('J',_('Judging')),
        ('M',_('Memory Limit Exceeded')),
        ('O',_('Output Limit Exceeded')),
        ('P',_('Presentation Error')),
        ('R',_('Runtime Error')),
        ('S',_('System Error(JUDGE)')),
        ('T',_('Time Limit Exceeded')),
        ('W',_('Wrong Answer')),
        ('U',_('Compiling Time Exceeded')),
        ('X',_('Compiling')),
        ('Z',_('Waiting')),
        #TODO:RUNTIME_ERROR(DIVIDED_BY_ZERO)
    )

    result = models.CharField(_("Result"), choices=RESULT_CHOICE, max_length=1)
    language = models.CharField(_("Programming language"), choices=PROGRAMMING_LANGUAGES, max_length=1)
    source_code = models.TextField(_("Source code"))

    submit_time = models.DateTimeField(_("Submit time"), auto_now_add=True)

    def __unicode__(self):
        return "Solution(Participant: " + str(self.participant) + ", " + str(self.problem) + ")"
