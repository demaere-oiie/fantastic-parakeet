from bezier import Bezier
from dataclasses import dataclass
from svg import connect

@dataclass
class Shape:
    bs: list[Bezier]

    def bxor(self, other):
        return Shape([b for b in self.bs if not b.covered(other.bs)] +
                     [b for b in other.bs if not b.covered(self.bs)])

    def beq(self, other):
        return not self.bxor(other).bs

    def band(self, other):
        return Shape(connect([r for b in self.bs for r in b.inside(other.bs)] +
                             [r for b in other.bs for r in b.inside(self.bs)]))
