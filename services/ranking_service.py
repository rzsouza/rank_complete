from match import Match


class RankingService:
    def __init__(self) -> None:
        self._ranking = []
        self._points: dict[str, int] = {}
        self._matches: list[Match] = []

    def _update_ranking(self, match: Match):
        home_points = 1
        away_points = 1

        if match.home_team_score > match.away_team_score:
            home_points = 3
            away_points = 0
        if match.home_team_score < match.away_team_score:
            home_points = 0
            away_points = 3

        self._points[match.home_team] = (
            self._points.get(match.home_team, 0) + home_points
        )
        self._points[match.away_team] = (
            self._points.get(match.away_team, 0) + away_points
        )

        self._ranking = sorted(
            self._points.items(), key=lambda item: item[1], reverse=True
        )

    def ranking(self):
        return self._ranking

    def add_match(self, match: Match):
        self._matches.append(match)
        self._update_ranking(match)
