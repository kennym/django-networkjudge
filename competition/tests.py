from django.utils import unittest
from django.test.client import Client

from competition.models import COMPETITION_STATUSES
from competition.models import Competition, Participant

class CompetitionTestCase(unittest.TestCase):
    fixtures = ['test_data.json']

    def _create_competition(self):
        competition = Competition.objects.create(title="test", description="test")
        return competition

    def test_start_competition(self):
        """
        Test the correct start of a competition
        """
        competition = self._create_competition()
        self.assertEquals(competition.status, COMPETITION_STATUSES[0][0])

        # Start competition
        competition.start(duration=30 * 60)
        self.assertEquals(competition.status, COMPETITION_STATUSES[1][0])

    def test_stop_competition(self):
        """
        Test the correct stop of a competition
        """
        competition = self._create_competition()

        # Start competition
        competition.start(duration=30 * 60)

        # Stop competition
        competition.stop()
        self.assertEquals(competition.status, COMPETITION_STATUSES[3][0])

    def test_reset_competition(self):
        """
        Test the correct reset of a competition
        """
        competition = self._create_competition()
        self.assertEquals(competition.status, COMPETITION_STATUSES[0][0])

        # Start competition
        competition.start(duration=30 * 60)
        self.assertEquals(competition.status, COMPETITION_STATUSES[1][0])

        competition.reset()
        self.assertEquals(competition.status, COMPETITION_STATUSES[0][0])
        self.assertEquals(competition.startTime, None)
        self.assertEquals(competition.endTime, None)

class ParticipantTestCase(unittest.TestCase):
    fixtures = ['test_data.json']

