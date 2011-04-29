from django.utils import unittest
from django.test.client import Client

import datetime

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
        self.assertNotEquals(competition.endTime, None)
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
    fixtures = ['initial_data.json']

    def setUp(self):
        pass

    def _create_solution(self, language, source_code, competition=None):
        if competition:
            competition = competition
        else:
            competition = Competition.objects.get(id=1)
        problem = Problem.objects.get(pk=1)
        participant = Participant.objects.get(pk=2)

        solution = Solution.objects.create(participant=participant, problem=problem, competition=competition,
                            language=language, source_code=source_code)
        solution.save()

        return solution

    def test_result_correct(self):
        language = PROGRAMMING_LANGUAGES[0][0]
        source_code = """
for i in xrange(1, 11):
    print i
"""
        solution = self._create_solution(language, source_code)
        solution.save()
        solution.compile_and_run()

        self.assertEquals(solution.result, Solution.RESULT_CHOICE[1][0])

        source_code = """
for i in xrange(1, 11):
    print i,
"""
        solution = self._create_solution(language, source_code)
        solution.save()
        solution.compile_and_run()

        self.assertEquals(solution.result, Solution.RESULT_CHOICE[1][0])

    def test_result_too_late(self):
        language = PROGRAMMING_LANGUAGES[0][0]
        source_code = """
for i in xrange(1, 11):
    print i
"""
        competition = Competition.objects.get(pk=1)
        competition.stop()

        solution = self._create_solution(language, source_code, competition=competition)
        solution.compile_and_run()
        solution.competition.reset() # To not cause obscure errors

        self.assertEquals(solution.result, Solution.RESULT_CHOICE[2][0])


    def test_result_compiler_error(self):
        language = PROGRAMMING_LANGUAGES[0][0]
        source_code = """
for i in xrange(1, 11):
    prin i # Syntax error
"""
        solution = self._create_solution(language, source_code)
        solution.compile_and_run()

        self.assertEquals(solution.result, Solution.RESULT_CHOICE[3][0])

    @unittest.SkipTest
    def test_result_time_limit_exceeded(self):
        pass

    @unittest.SkipTest
    def test_result_output_limit_passed(self):
        pass

    def test_result_no_output(self):
        language = PROGRAMMING_LANGUAGES[0][0]
        source_code = """
for i in xrange(1, 11):
    pass
"""
        solution = self._create_solution(language, source_code)
        solution.compile_and_run()

        self.assertEquals(solution.result, Solution.RESULT_CHOICE[5][0])

    def test_result_wrong_answer(self):
        language = PROGRAMMING_LANGUAGES[0][0]
        source_code = """
for i in xrange(1, 5):
    print i
"""
        solution = self._create_solution(language, source_code)
        solution.compile_and_run()

        self.assertEquals(solution.result, Solution.RESULT_CHOICE[6][0])

    def test_result_invalid_submission(self):
        """TODO: Handle invalid submissions correctly"""
        language = PROGRAMMING_LANGUAGES[0][0]
        source_code = """
for i in xrange(1, 11):
    print i
"""
        # First create a correct solution
        solution = self._create_solution(language, source_code)
        solution.compile_and_run()

        self.assertEquals(solution.result, Solution.RESULT_CHOICE[1][0])

        # Then create another solution for the same problem
        solution = self._create_solution(language, source_code)
        solution.compile_and_run()

        self.assertEquals(solution.result, Solution.RESULT_CHOICE[7][0])

#    def test_result_presentation_error(self):
#        pass

