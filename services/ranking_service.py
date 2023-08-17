from typing import List

from models.match import Match
from models.match_graph import MatchGraph, Ranking


class RankingService:
    def __init__(self) -> None:
        self._ranking: Ranking = []
        self._matches: List[Match] = []

    def ranking(self) -> Ranking:
        return self._ranking

    def add_match(self, match: Match) -> Ranking:
        self._matches.append(match)
        graph = MatchGraph(self._matches)
        self._ranking = graph.ranking()
        return self._ranking
