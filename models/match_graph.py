from typing import TypeAlias

from models.match import Match

MatchMap: TypeAlias = dict[str, Match]
TeamMap: TypeAlias = dict[str, MatchMap]


def _build_graph(matches: list[Match]) -> TeamMap:
    team_map: TeamMap = {}
    for match in matches:
        games: MatchMap = team_map.get(match.home_team, {})
        games[match.away_team] = match
        team_map[match.home_team] = games
        games: MatchMap = team_map.get(match.away_team, {})
        games[match.home_team] = match
        team_map[match.away_team] = games

    return team_map


class MatchGraph:
    def __init__(self, matches: list[Match]) -> None:
        self._graph: TeamMap = _build_graph(matches)

    @property
    def team_map(self) -> TeamMap:
        return self._graph
