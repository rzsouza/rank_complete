from typing import TypeAlias

from models.match import Match
from models.ranking_stats import RankingStats

MatchMap: TypeAlias = dict[str, Match]
TeamMap: TypeAlias = dict[str, MatchMap]
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
    return sorted(
        list(graph.values()),
        key=lambda stats: (-stats.total_points, -stats.real_points, stats.name),
    )


def _build_ranking(matches: list[Match]) -> Ranking:
    team_map: TeamMap = {}
    for match in matches:
        games: MatchMap = team_map.get(match.home_team, {})
        games[match.away_team] = match
        team_map[match.home_team] = games
        games: MatchMap = team_map.get(match.away_team, {})
        games[match.home_team] = match
        team_map[match.away_team] = games

    graph: dict[str, RankingStats] = {}
    for team in team_map.keys():
        graph[team] = calculate_points(team, team_map)

    return _sort_graph(graph)


class MatchGraph:
    def __init__(self, matches: list[Match]) -> None:
        self._ranking: Ranking = _build_ranking(matches)

    def ranking(self) -> Ranking:
        return self._ranking
