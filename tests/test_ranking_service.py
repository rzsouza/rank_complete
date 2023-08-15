from unittest import TestCase

from match import Match
from services.ranking_service import RankingService


class TestRankingService(TestCase):
    def test_ranking_starts_with_empty_ranking(self):
        service = RankingService()
        self.assertEqual(service.ranking(), [], "ranking should be empty")

    def test_draw_should_have_teams_with_one_point(self):
        service = RankingService()
        match = Match("Brazil", 0, "Argentina", 0)
        service.add_match(match)

        ranking = service.ranking()
        self.assertEqual(len(ranking), 2, "should have 2 teams ranked")

        for team in ranking:
            self.assertEqual(team[1], 1, "should have 1 point")

    def test_win_should_have_teams_with_2_and_0_points(self):
        service = RankingService()
        match = Match("Italy", 2, "Germany", 0)
        service.add_match(match)

        ranking = service.ranking()
        self.assertEqual(len(ranking), 2, "should have 2 teams ranked")

        italy = ranking[0]
        self.assertEqual(italy[1], 3, "should have 3 point")

        germany = ranking[1]
        self.assertEqual(germany[1], 0, "should have 0 point")
