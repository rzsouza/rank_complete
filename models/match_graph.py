from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias

from models.match import Match

MatchMap: TypeAlias = dict[str, Match]
TeamMap: TypeAlias = dict[str, MatchMap]


class PointType(Enum):
    REAL = 0
    TRANSITIVE = 1
    UNKNOWN = 2


@dataclass
class PointResult:
    points: int
    point_type: PointType


class MatchResult(Enum):
    LOSS = 0
    DRAW = 1
    WIN = 3


class Edge:
    def __init__(self, match: Match):
        self._edge: dict[str, MatchResult] = {}
        if match.home_team_score == match.away_team_score:
            self._edge[match.home_team] = MatchResult.DRAW
            self._edge[match.away_team] = MatchResult.DRAW
        elif match.home_team_score > match.away_team_score:
            self._edge[match.home_team] = MatchResult.WIN
            self._edge[match.away_team] = MatchResult.LOSS
        else:
            self._edge[match.home_team] = MatchResult.LOSS
            self._edge[match.away_team] = MatchResult.WIN

    def __getitem__(self, item):
        return self._edge[item]


class MatchGraph:
    def __init__(self, matches: list[Match]) -> None:
        self._graph: dict[str, dict[str, Edge]] = {}
        for match in matches:
            self._update_graph(match)

    def _update_graph(self, match):
        edge = Edge(match)
        home_graph = self._graph.get(match.home_team, {})
        home_graph[match.away_team] = edge
        self._graph[match.home_team] = home_graph
        away_graph = self._graph.get(match.away_team, {})
        away_graph[match.home_team] = edge
        self._graph[match.away_team] = away_graph

    @property
    def teams(self) -> list[str]:
        return list(self._graph.keys())

    def find_result(self, team1, team2) -> PointResult:
        team1_edges = self._graph[team1]

        if team2 in team1_edges:
            return PointResult(team1_edges[team2][team1].value, PointType.REAL)

        return PointResult(1, PointType.UNKNOWN)
