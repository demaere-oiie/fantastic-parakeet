from bezier import Bezier
from dataclasses import dataclass
from topo import connect, trim

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
        return not trim(nontriv(self.bxor(other).bs))

    def band(self, other):
        return Shape(connect(
            [r for b in self.bs
               for r in b.inside(other.bs,None)] +
            [r for b in other.bs
               for r in b.inside(self.bs,other.bs)]) or
                     connect(
            [r for b in self.bs
               for r in b.inside(other.bs,self.bs)] +
            [r for b in other.bs
               for r in b.inside(self.bs,None)]))

    def ble(self, other):
        return self.band(other).beq(self)

    def bor(self, other):
        return self.band(other).bxor(self.bxor(other))

    def db_and(self, other):
        from svg import svgout3
        for r in self.bs:
            print("s",r)
        for r in other.bs:
            print("o",r)
        for r in [r for b in self.bs 
                    for r in b.inside(other.bs,None)]:
            print("0",r)
        for r in [r for b in other.bs
                    for r in b.inside(self.bs,other.bs)]:
            print("1",r)
        for r in [r for b in self.bs
                    for r in b.inside(other.bs,self.bs)]:
            print("2",r)
        svgout3([r for b in self.bs for r in b.inside(other.bs,None)]+
                [r for b in other.bs for r in b.inside(self.bs,other.bs)])
        svgout3([r for b in self.bs for r in b.inside(other.bs,self.bs)]+
                [r for b in other.bs for r in b.inside(self.bs,None)])
        return self.band(other)

    def db_xor(self, other):
        print("----")
        for b in self.bs:
          print("b",b)
          for u in b.uncovered(other.bs):
            print("u",u)
            for r in u.splitsBy(other.bs):
              print(":",r)
        print("----")
        for b in other.bs:
          print("b",b)
          for u in b.uncovered(self.bs):
            print("u",u)
            for r in u.splitsBy(self.bs):
              print(":",r)
        return self.bxor(other)

def nontriv(bs):
    return [b for b in bs if not b.b0.close(b.b3,1e3)]
