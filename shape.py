from bezier import Bezier
from dataclasses import dataclass
from svg import connect

@dataclass
class Shape:
    bs: list[Bezier]

    def bxor(self, other):
        return Shape([r for b in self.bs for r in b.uncovered(other.bs)] +
                     [r for b in other.bs for r in b.uncovered(self.bs)])

    def beq(self, other):
        return not self.bxor(other).bs

    def band(self, other):
        return Shape(connect(
            [r for b in self.bs for r in b.inside(other.bs,0)] +
            [r for b in other.bs for r in b.inside(self.bs,1)]))

    def bor(self, other):
        return self.band(other).bxor(self.bxor(other))
