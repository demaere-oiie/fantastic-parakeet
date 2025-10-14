from bezier import Bezier
from dataclasses import dataclass
from svg import connect

@dataclass
class Shape:
    bs: list[Bezier]

    def bxor(self, other):
        return Shape(nontriv(
                     [r for b in self.bs
                        for u in b.uncovered(other.bs)
                        for r in u.splitsBy(other.bs)] +
                     [r for b in other.bs
                        for u in b.uncovered(self.bs)
                        for r in u.splitsBy(self.bs)]))

    def beq(self, other):
        return not self.bxor(other).bs

    def band(self, other):
        return Shape(connect(
            [r for b in self.bs for r in b.inside(other.bs,0)] +
            [r for b in other.bs for r in b.inside(self.bs,1)]))

    def ble(self, other):
        return self.band(other).beq(self)

    def bor(self, other):
        return self.band(other).bxor(self.bxor(other))

    def db_and(self, other):
        for r in [r for b in self.bs for r in b.inside(other.bs,0)]:
            print("0",r)
        for r in [r for b in other.bs for r in b.inside(self.bs,1)]:
            print("1",r)
        return self.band(other)

def nontriv(bs):
    return [b for b in bs if not b.b0.close(b.b3,1e3)]
