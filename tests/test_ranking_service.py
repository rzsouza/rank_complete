from typing import List, Tuple
from unittest import TestCase

from match import Match
from services.ranking_service import RankingService


class TestRankingService(TestCase):
    def test_ranking_starts_with_empty_ranking(self):
        service = RankingService()
        self.assert_ranks_match_expected([], service.ranking())

    def test_draw_should_have_teams_with_one_point(self):
        service = RankingService()
        match = Match("Brazil", 0, "Argentina", 0)
        service.add_match(match)

        expected_ranking = [("Brazil", 1), ("Argentina", 1)]

        self.assert_ranks_match_expected(expected_ranking, service.ranking())

    def test_win_should_have_teams_with_3_and_0_points(self):
        service = RankingService()
        match = Match("Italy", 2, "Germany", 0)
        service.add_match(match)

        expected_ranking = [("Italy", 3), ("Germany", 0)]

        self.assert_ranks_match_expected(expected_ranking, service.ranking())

    def assert_ranks_match_expected(
        self,
        expected_ranking: List[Tuple],
        ranking: List[Tuple],
    ):
        self.assertEqual(len(expected_ranking), len(ranking), "should have same length")

        for index, line in enumerate(ranking):
            self.assertEqual(expected_ranking[index], line)
