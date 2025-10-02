from util import Eps, mid, close
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

    def close(self, other, s=2):
        return abs(self.x-other.x)<s*Eps and abs(self.y-other.y)<s*Eps

    def lerp(self, other, t):
        return Point(self.x + t*(other.x-self.x),
                     self.y + t*(other.y-self.y))

@dataclass
class Bezier:
    b0: Point
    b1: Point
    b2: Point
    b3: Point

    def bbox(self):
        return (min(p.x for p in [self.b0,self.b1,self.b2,self.b3]),
                min(p.y for p in [self.b0,self.b1,self.b2,self.b3]),
                max(p.x for p in [self.b0,self.b1,self.b2,self.b3]),
                max(p.y for p in [self.b0,self.b1,self.b2,self.b3]))

    def split(self, t):
        q0 = self.b0.lerp(self.b1,t)
        q1 = self.b1.lerp(self.b2,t)
        q2 = self.b2.lerp(self.b3,t)
        r0 = q0.lerp(q1,t)
        r1 = q1.lerp(q2,t)
        s  = r0.lerp(r1,t)
        return [Bezier(self.b0,q0,r0,s),Bezier(s,r1,q2,self.b3)]

    def eval(self, t):
        [b,c] = self.split(t)
        return b.b3

    def isect(self, other):
        a, b = self, other
        xs,ms = isect_raw([(a,b,0.,1.,0.,1.,'d')],a,b,0)
        us = []
        for b1,b2,ta,to,ua,uo,xx in xs:
             if xx=='x':
                  t = mid(ta,to)
                  if not any(close(t,u) for u in us):
                       us.append(t)
        return (us,ms)

def merge(xs):
    # it's wrong, but for now assume at most one overlap
    ta, to = 1.0, 0.0
    for b1,b2,xta,xto,xua,xuo,xx in xs:
        ta = min(ta,xta)
        to = max(to,xto)
    return [(ta,to)]

def isect_raw(xs, a, b, n):
    if len(xs) > 1000: #45:
        return (xs, merge(xs))
    else:
        ys = [r
          for _ in [min]
          for meas in [lambda w: _(xo-xa+yo-ya
                              for xa,ya,xo,yo in [w])]
          for area in [lambda w: _((xo-xa)*(yo-ya)
                              for xa,ya,xo,yo in [w])]
          for very_small in [lambda w: _((xo-xa<=Eps) and (yo-ya<=Eps)
                              for xa,ya,xo,yo in [w])]
          for disjoint in [lambda b,c: _( bxo < cxa or cxo < bxa or
                                          byo < cya or cyo < bya
              for bxa,bya,bxo,byo in [b]
              for cxa,cya,cxo,cyo in [c])]

            for b1,b2,ta,to,ua,uo,xx in xs
            for bb1 in [b1.bbox()]
            for bb2 in [b2.bbox()]
          for st,su in [(0.5,0.5)]
          for b11,b12 in [b1.split(st)]
          for b21,b22 in [b2.split(su)]
          for small_bb1 in [very_small(bb1) or b11==b1]
          for small_bb2 in [very_small(bb2) or b21==b2]
          for r in ([] if (ta>to or ua>uo or disjoint(bb1,bb2)) else
              [(b1,b2,ta,to,ua,uo,'x')] if
                  small_bb1 and small_bb2 and area(bb1) + area(bb2) <= Eps else
            _([(b1,b21,ta,to,ua,um,''),
               (b1,b22,ta,to,um,uo,'')]
                   for um in [mid(ua,uo)]) if meas(bb1) < meas(bb2) else
            _([(b11,b2,ta,tm,ua,uo,''),
               (b12,b2,tm,to,ua,uo,'')]
                   for tm in [mid(ta,to)])) ]
    if xs == ys:
        return (xs, [])
    return isect_raw(ys, a, b, n+1)
