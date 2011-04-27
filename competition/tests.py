from django.utils import unittest
from django.test.client import Client

from competition.models import COMPETITION_STATUSES
from competition.models import (
    Competition,
    Participant,
    Problem,
    Solution,
    Team,
    PROGRAMMING_LANGUAGES
)

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

class SolutionTest(unittest.TestCase):
    def _create_solution(self, language, source_code):
        competition = Competition.objects.get(pk=1)
        problem = Problem.objects.get(pk=1)
        participant = Participant.objects.get(pk=2)

        solution = Solution(participant=participant, problem=problem, competition=competition,
                            language=language, source_code=source_code)
        solution.save()
        return solution

    def test_result_correct(self):
        language = PROGRAMMING_LANGUAGES[0][0]
        source_code = """
for i in xrange(1, 10):
    print i
"""
        solution = self._create_solution(language, source_code)
        solution.save()
        solution.compile_and_run()

        print solution.error_message
        self.assertEquals(solution.result, Solution.RESULT_CHOICE[1][1])

    def test_result_too_late(self):
        pass

    def test_result_compiler_error(self):
        pass

    def test_result_time_limit_exceeded(self):
        pass

    def test_result_output_limit_passed(self):
        pass

    def test_result_no_output(self):
        pass

    def test_result_wrong_answer(self):
        pass

    def test_result_invalid_submission(self):
        pass

#    def test_result_presentation_error(self):
#        pass

