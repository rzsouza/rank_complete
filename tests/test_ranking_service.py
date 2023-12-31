from typing import List
from unittest import TestCase

from models.match import Match
from models.ranking_stats import RankingStats
from services.ranking_service import RankingService, SortedRanking


class TestRankingService(TestCase):
    def test_ranking_starts_with_empty_ranking(self):
        self.assert_ranks_match_expected([], [])

    def test_draw_should_have_teams_with_one_point(self):
        matches = [Match("Brazil", 0, "Argentina", 0)]

        expected_ranking = [
            (1, RankingStats("Argentina", 0, 0, 1)),
            (1, RankingStats("Brazil", 0, 0, 1)),
        ]

        self.assert_ranks_match_expected(expected_ranking, matches)

    def test_win_should_have_teams_with_3_and_0_points(self):
        matches = [Match("Italy", 2, "Germany", 0)]
        expected_ranking = [
            (1, RankingStats("Italy", 0, 0, 3)),
            (2, RankingStats("Germany", 0, 0, 0)),
        ]

        self.assert_ranks_match_expected(expected_ranking, matches)

    def test_teams_in_different_graphs_should_generate_unknown_points(self):
        matches = [
            Match("Italy", 2, "Germany", 0),
            Match("Brazil", 1, "France", 1),
        ]

        expected_ranking = [
            (1, RankingStats("Italy", 2, 0, 3)),
            (2, RankingStats("Brazil", 2, 0, 1)),
            (2, RankingStats("France", 2, 0, 1)),
            (4, RankingStats("Germany", 2, 0, 0)),
        ]

        self.assert_ranks_match_expected(expected_ranking, matches)

    def test_transitive_points(self):
        matches = [
            Match("Italy", 2, "Germany", 0),
            Match("Italy", 1, "France", 1),
        ]

        expected_ranking = [
            (1, RankingStats("Italy", 0, 0, 4)),
            (2, RankingStats("France", 0, 3, 1)),
            (3, RankingStats("Germany", 0, 0, 0)),
        ]

        self.assert_ranks_match_expected(expected_ranking, matches)

    def assert_ranks_match_expected(
        self,
        expected_ranking: SortedRanking,
        matches: List[Match],
    ):
        service = RankingService()

        for match in matches:
            service.add_match(match)

        ranking = service.ranking
        self.assertEqual(len(expected_ranking), len(ranking), "should have same length")

        for index, line in enumerate(ranking):
            self.assertEqual(expected_ranking[index], line)
