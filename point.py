from dataclasses import dataclass

Eps = 1e-5

@dataclass
class Point:
    x: float
    y: float

    def near(self, other, s=2):
        return abs(self.x-other.x)<s*Eps and abs(self.y-other.y)<s*Eps

    def lerp(self, other, t):
        return Point(self.x + t*(other.x-self.x),
                     self.y + t*(other.y-self.y))
