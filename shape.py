from dataclasses import dataclass

from bezier import Bezier
from math   import pi, sin, cos
from point  import Point
from topo   import connect, trim

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

    def band(self, other, last_pass=False):
        return Shape(connect(
            [r for b in self.bs  for r in other.inside(b, None)] +
            [r for b in other.bs for r in self.inside(b, other)]) or
            ([] if last_pass else other.band(self, True).bs))

    def beq(self, other):
        return not trim(nontriv(self.bxor(other).bs))

    def ble(self, other):
        return self.band(other).beq(self)

    def bor(self, other):
        return self.band(other).bxor(self.bxor(other))

    def inside(self, bez, other=None):
        self, others, selves = bez, self.bs, (other and other.bs)
        isects, olaps, keeps = [],[],[]
        for y in others:
            i,o = self.isectB(y)
            isects.extend(i)
            olaps.extend(o)
        c = connect(others)
        for o,p in zip(c,c[1:]+c[:1]):
            isects.extend(self.isectB(Bezier(o.b3,o.b3,p.b0,p.b0))[0])
        isects = sorted((i for i in isects
                        if not Point(i,0).near(Point(0,0),1e3) and
                           not Point(i,0).near(Point(1,0),1e3)))
        for a,o in zip([0.]+isects,isects+[1.]):
            sb = self.subbez(a,o)

            overlapped = False
            for (xa,xo) in olaps:
                if selves is not None and Point(xa,xo).near(Point(0,1),1e3):
                    if self.testRay().testEdge(others,selves):
                        keeps.append(self)
                    overlapped = True
                    break
                elif Point(xa,xo).near(Point(a,o),1e3):
                    if selves is not None:
                        if Point(xa,xo).near(Point(0.,1.),1e3):
                            xa,xo = 0,1
                        if self.subbez(xa,xo).testRay().testEdge(others,selves):
                            keeps.append(sb)
                    overlapped = True
                    break

            if not (overlapped or sb.testRay().testEdge(others,[])):
                keeps.append(sb)

        return nontriv(keeps,1)

    def translate(self, x, y):
        return Shape([Bezier(Point(b.b0.x+x,b.b0.y+y),
                             Point(b.b1.x+x,b.b1.y+y),
                             Point(b.b2.x+x,b.b2.y+y),
                             Point(b.b3.x+x,b.b3.y+y)) for b in self.bs])

    def scale(self, v):
        return Shape([Bezier(Point(b.b0.x*v,b.b0.y*v),
                             Point(b.b1.x*v,b.b1.y*v),
                             Point(b.b2.x*v,b.b2.y*v),
                             Point(b.b3.x*v,b.b3.y*v)) for b in self.bs])

    def rot(self, a):
        rad = a * (pi/180)
        c, s = cos(rad), sin(rad)
        return Shape([Bezier(Point(b.b0.x*c - b.b0.y*s,
                                   b.b0.x*s + b.b0.y*c),
                             Point(b.b1.x*c - b.b1.y*s,
                                   b.b1.x*s + b.b1.y*c),
                             Point(b.b2.x*c - b.b2.y*s,
                                   b.b2.x*s + b.b2.y*c),
                             Point(b.b3.x*c - b.b3.y*s,
                                   b.b3.x*s + b.b3.y*c))
                             for b in self.bs])

def nontriv(bs,s=1e3):
    return [b for b in bs if not b.b0.near(b.b3,s)]
