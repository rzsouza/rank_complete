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
    DRAW = 0
    WIN = 1
    LOSS = 2


class Edge:
    def __init__(self, match: Match):
        self._edge: dict[str, MatchResult] = {}
        if match.home_team_score == match.away_team_score:
            self._edge[match.home_team] = MatchResult.DRAW
            self._edge[match.away_team] = MatchResult.DRAW
        elif match.away_team_score > match.away_team_score:
            self._edge[match.home_team] = MatchResult.WIN
            self._edge[match.away_team] = MatchResult.LOSS
        else:
            self._edge[match.home_team] = MatchResult.LOSS
            self._edge[match.away_team] = MatchResult.WIN


class MatchGraph:
    _graph: dict[str, Edge] = {}

    def __init__(self, matches: list[Match]) -> None:
        for match in matches:
            edge = Edge(match)
            self._graph[match.home_team] = edge
            self._graph[match.away_team] = edge

    @property
    def teams(self) -> list[str]:
        return list(self._graph.keys())

    @staticmethod
    def find_result() -> PointResult:
        return PointResult(1, PointType.UNKNOWN)
