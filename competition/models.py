# coding=utf-8

from django.db import models
from django.contrib.auth.models import User, UserManager

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

    def __unicode__(self):
        return self.title


class Judge(models.Model):
    """
    Judge model base class.
    """
    competition = models.ForeignKey(Competition)
    
    class Meta:
        abstract = True
        

class HumanJudge(Judge, User):
    """
    HumanJudge model.

    A human judge can only belong to a single competition.

    """
    objects = UserManager()


class ComputerJudge(Judge):
    """
    ComputerJudge model.

    A computer judge (AI) can only belong to a single competition.

    """
    name = models.CharField(max_length="20")


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

    title = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return "Problem(" + self.title + ")"


class Solution(models.Model):
    """
    Solution model
    """
    participant = models.OneToOneField(Participant)
    problem = models.OneToOneField(Problem)

    file = models.FileField(upload_to='solutions')

    submissionDate = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Solution(Participant: " + str(self.participant) + ", " + str(self.problem) + ")"
