from operator import attrgetter
from typing import List, TypeAlias

from models.match import Match
from models.match_graph import MatchGraph, TeamMap
from models.ranking_stats import RankingStats

Ranking: TypeAlias = list[RankingStats]


def _calculate_match_points(match: Match) -> tuple[int, int]:
    if match.home_team_score > match.away_team_score:
        return 3, 0
    if match.home_team_score < match.away_team_score:
        return 0, 3
    return 1, 1


def calculate_points(team: str, team_map) -> RankingStats:
    real_points = 0
    unknown_points = 0
    team_matches = team_map[team]
    for other_team in team_map.keys():
        if other_team in team_matches.keys():
            match = team_matches[other_team]
            (home_team_points, away_team_points) = _calculate_match_points(match)
            team_points = (
                home_team_points if team == match.home_team else away_team_points
            )
            real_points += team_points
        elif other_team != team:
            unknown_points += 1

    return RankingStats(team, unknown_points, 0, real_points)


def _sort_graph(graph: dict[str, RankingStats]) -> Ranking:
    result = sorted(list(graph.values()), key=attrgetter("name"))
    return sorted(
        result,
        key=attrgetter("total_points", "real_points", "transitive_points"),
        reverse=True,
    )


class RankingService:
    def __init__(self) -> None:
        self._ranking: Ranking = []
        self._matches: List[Match] = []

    def _update_ranking(self, team_map: TeamMap):
        graph: dict[str, RankingStats] = {}
        for team in team_map.keys():
            graph[team] = calculate_points(team, team_map)

        self._ranking = _sort_graph(graph)

    def ranking(self) -> Ranking:
        return self._ranking

    def add_match(self, match: Match) -> Ranking:
        self._matches.append(match)
        graph = MatchGraph(self._matches)
        self._update_ranking(graph.team_map)
        return self._ranking
