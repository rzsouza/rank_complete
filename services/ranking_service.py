from operator import attrgetter
from typing import List, TypeAlias

from models.match import Match
from models.match_graph import MatchGraph, PointType
from models.ranking_stats import RankingStats

Ranking: TypeAlias = list[RankingStats]
SortedRanking: TypeAlias = list[tuple[int, RankingStats]]


def _sort_ranking(graph: dict[str, RankingStats]) -> SortedRanking:
    ranking_stats = sorted(list(graph.values()), key=attrgetter("name"))
    ranking_stats = sorted(
        ranking_stats,
        key=attrgetter("total_points", "real_points", "transitive_points"),
        reverse=True,
    )

    result: SortedRanking = []
    rank = 0
    for index, team_stats in enumerate(ranking_stats):
        if index == 0 or team_stats != ranking_stats[index - 1]:
            rank = index + 1
        result.append((rank, team_stats))

    return result


class RankingService:
    def __init__(self) -> None:
        self._ranking: SortedRanking = []
        self._matches: List[Match] = []
        self._graph = MatchGraph([])

    def update_ranking(self):
        results_by_team: dict[str, RankingStats] = {}

        for team1 in self._graph.teams:
            real_points = 0
            unknown_points = 0
            transitive_points = 0

            for team2 in self._graph.teams:
                if team1 == team2:
                    continue

                result = self._graph.find_result(team1, team2)
                if result.point_type == PointType.REAL:
                    real_points += result.points
                elif result.point_type == PointType.UNKNOWN:
                    unknown_points += result.points
                elif result.point_type == PointType.TRANSITIVE:
                    transitive_points += result.points

            results_by_team[team1] = RankingStats(
                team1, unknown_points, transitive_points, real_points
            )

        self._ranking = _sort_ranking(results_by_team)

    @property
    def ranking(self) -> SortedRanking:
        return self._ranking

    def add_match(self, match: Match) -> None:
        self._matches.append(match)
        self._graph = MatchGraph(self._matches)
        self.update_ranking()
