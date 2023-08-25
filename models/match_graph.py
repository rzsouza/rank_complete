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


@dataclass
class Path:
    result: MatchResult
    path: list[str]


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


def find_path_ending_with_team(game_paths: list[Path], team2: str) -> Path | None:
    for path in game_paths:
        if path.path[-1] == team2:
            return path
    return None


def find_new_result(
    current_result: MatchResult, new_result: MatchResult
) -> tuple[bool, MatchResult | None]:
    if current_result == MatchResult.DRAW:
        return True, new_result

    if current_result == MatchResult.WIN:
        if new_result == MatchResult.LOSS:
            return False, None
        else:
            return True, MatchResult.WIN

    if current_result == MatchResult.LOSS:
        if new_result == MatchResult.WIN:
            return False, None
        else:
            return True, MatchResult.LOSS


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

    def find_result(self, team1: str, team2: str) -> PointResult:
        checked_teams: set[str] = {team1}
        game_paths: list[Path] = [Path(result=MatchResult.DRAW, path=[team1])]

        can_expand = True
        while (find_path_ending_with_team(game_paths, team2) is None) and can_expand:
            game_paths, checked_teams, can_expand = self.expand_game_paths(
                game_paths, checked_teams
            )

        path = find_path_ending_with_team(game_paths, team2)

        if path is None:
            return PointResult(1, PointType.UNKNOWN)

        if len(path.path) <= 2:
            return PointResult(path.result.value, PointType.REAL)
        else:
            return PointResult(path.result.value, PointType.TRANSITIVE)

    def expand_game_paths(
        self, game_paths: list[Path], checked_teams: set[str]
    ) -> tuple[list[Path], set[str], bool]:
        new_checked_teams: set[str] = set()
        new_game_paths: list[Path] = []

        for path in game_paths:
            last_team = path.path[-1]

            last_team_edges = self._graph[last_team]
            for new_last_team in last_team_edges:
                if new_last_team not in checked_teams:
                    is_transitive_new_result, new_result = find_new_result(
                        path.result, last_team_edges[new_last_team][last_team]
                    )

                    if is_transitive_new_result:
                        new_game_paths.append(
                            Path(result=new_result, path=path.path + [new_last_team])
                        )

                    new_checked_teams.add(new_last_team)

        new_checked_teams = new_checked_teams.union(checked_teams)

        return new_game_paths, new_checked_teams, new_checked_teams != checked_teams
