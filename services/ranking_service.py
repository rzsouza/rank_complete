from match import Match


class RankingService:
    _ranking = []

    points: dict[str, int] = {}

    matches: list[Match] = []

    def _update_ranking(self, match: Match):
        home_points = 1
        away_points = 1

        if match.home_team_score > match.away_team_score:
            home_points = 3
            away_points = 0
        if match.home_team_score < match.away_team_score:
            home_points = 0
            away_points = 3

        self.points[match.home_team] = self.points.get(match.home_team, 0) + home_points
        self.points[match.away_team] = self.points.get(match.away_team, 0) + away_points

        self._ranking = sorted(
            self.points.items(), key=lambda item: item[1], reverse=True
        )

    def ranking(self):
        return self._ranking

    def add_match(self, match: Match):
        self.matches.append(match)
        self._update_ranking(match)
