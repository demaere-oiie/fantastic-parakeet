from bezier import Bezier
from dataclasses import dataclass

@dataclass
class Shape:
    bs: list[Bezier]

    def bxor(self, other):
        return Shape([b for b in self.bs if not b.covered(other.bs)] +
                     [b for b in other.bs if not b.covered(self.bs)])

    def beq(self, other):
        return not bxor(self, other).bs
