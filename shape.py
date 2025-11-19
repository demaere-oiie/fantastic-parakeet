from dataclasses import dataclass

from bezier import Bezier
from math   import pi, sin, cos
from point  import Point
from topo   import connect, trim

def xform(bs,f):
    return Shape([Bezier(f(b.b0),f(b.b1),f(b.b2),f(b.b3)) for b in bs])

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

    def watertight(self):
        xs = connect(self.bs)
        ys = []
        z = 0
        for i,x in enumerate(xs):
            if x.b3.near(xs[z].b0):
                ys.append(Bezier(x.b0,x.b1,x.b2,xs[z].b0))
                print("loop",z,i+1)
                z = i+1
            elif i+1<len(xs):
                ys.append(Bezier(x.b0,x.b1,x.b2,xs[i+1].b0))
            else:
                print("!!!!!")
                ys.append(x)
        if z!=len(xs): print("???")
        return Shape(ys[:z])

    def translate(self, x, y):
        return xform(self.bs, lambda p: Point(p.x+x, p.y+y))

    def scale(self, v):
        return xform(self.bs, lambda p: Point(p.x*v, p.y*v))

    def rot(self, a):
        rad = a * (pi/180)
        c, s = cos(rad), sin(rad)
        return xform(self.bs, lambda p: Point(p.x*c - p.y*s, p.x*s + p.y*c))

    def curl(self, wid):
        rad = -9.5 * wid * (pi/180)
        return xform(self.bs,
            lambda p: Point(-p.y * cos(p.x/rad),
                            -p.y * sin(p.x/rad)))

    def spiral(self):
        rad = -200 * (pi/180)
        return xform(self.bs,
            lambda p: Point(-p.y * (1+(p.x/10*rad)) * cos(p.x/rad),
                            -p.y * (1+(p.x/10*rad)) * sin(p.x/rad)))


def nontriv(bs,s=1e3):
    return [b for b in bs if not b.b0.near(b.b3,s)]
