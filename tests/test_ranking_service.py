from typing import List
from unittest import TestCase

from models.match import Match
from models.ranking_stats import RankingStats
from services.ranking_service import RankingService


class TestRankingService(TestCase):
    def test_ranking_starts_with_empty_ranking(self):
        self.assert_ranks_match_expected([], [])

    def test_draw_should_have_teams_with_one_point(self):
        matches = [Match("Brazil", 0, "Argentina", 0)]

        expected_ranking = [
            RankingStats("Brazil", 0, 1),
            RankingStats("Argentina", 0, 1),
        ]

        self.assert_ranks_match_expected(expected_ranking, matches)

    def test_win_should_have_teams_with_3_and_0_points(self):
        matches = [Match("Italy", 2, "Germany", 0)]
        expected_ranking = [
            RankingStats("Italy", 0, 3),
            RankingStats("Germany", 0, 0),
        ]

        self.assert_ranks_match_expected(expected_ranking, matches)

    def test_same_team_plays_twice_appears_only_once_in_ranking(self):
        matches = [
            Match("Italy", 2, "Germany", 0),
            Match("Italy", 1, "France", 1),
        ]

        expected_ranking = [
            RankingStats("Italy", 0, 4),
            RankingStats("France", 3, 1),
            RankingStats("Germany", 0, 0),
        ]

        self.assert_ranks_match_expected(expected_ranking, matches)

    def assert_ranks_match_expected(
        self,
        expected_ranking: List[RankingStats],
        matches: List[Match],
    ):
        service = RankingService()

        ranking = []
        for match in matches:
            ranking = service.add_match(match)

        self.assertEqual(len(expected_ranking), len(ranking), "should have same length")

        for index, line in enumerate(ranking):
            self.assertEqual(expected_ranking[index], line)
