from dataclasses import dataclass


@dataclass
class RankingStats:
    name: str
    unknown_points: int
    transitive_points: int
    real_points: int

    @property
    def total_points(self) -> int:
        return self.real_points + self.transitive_points + self.unknown_points
