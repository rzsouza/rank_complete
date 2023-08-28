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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RankingStats):
            return False
        return (
            self.real_points == other.real_points
            and self.transitive_points == other.transitive_points
            and self.unknown_points == other.unknown_points
        )
