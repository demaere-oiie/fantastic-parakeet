from dataclasses import dataclass

from bezutil import isect_raw, mid, xor1d
from point   import Point

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

    def subbez(self, a, o):
        return self.split(o)[0].split(a/o)[1]

    def isectB(self, other):
        a, b = self, other
        xs,ms = isect_raw([(a,b,0.,1.,0.,1.,'d')],a,b,0)
        ys, ps = [], []
        for b1,b2,ta,to,ua,uo,xx in xs:
            if xx=='x':
                t = mid(ta,to)
                q = a.eval(t)
                if not any(q.near(p,1e2) for p in ps):
                    ys.append(t)
                    ps.append(q)
        return (ys,ms)

    def uncovered(self, others):
        olap = [0.,1.]
        for c in others:
            olap = xor1d(olap,[r for m in self.isectB(c)[1] for r in m[:2]])
        if olap == [0.,1.]: return [self]
        return [self.subbez(a,o) for (a,o) in zip(olap[0::2],olap[1::2])]

    def splitsBy(self, others):
        isects, keeps = [], []
        for y in others:
            i,o = self.isectB(y)
            isects.extend(self.isectB(y)[0])
            isects.extend(self.isectB(Bezier(y.b0,y.b0,y.b0,y.b0))[0])
            isects.extend(self.isectB(Bezier(y.b3,y.b3,y.b3,y.b3))[0])
        isects = sorted((i for i in isects
                        if not Point(i,0).near(Point(0,0),1e3) and
                           not Point(i,0).near(Point(1,0),1e3)))
        for a,o in zip([0.]+isects,isects+[1.]):
            keeps.append(self.subbez(a,o))
        return [k for k in  keeps if not k.b0.near(k.b3)]

    def testRay(self):
        p = self.eval(0.5)
        dx,dy = (500,0)
        return Bezier(Point(p.x-0.001,p.y),Point(p.x+dx,p.y+dy),
                      Point(p.x+dx,p.y+dy),Point(p.x+2*dx,p.y+2*dy))

    def testEdge(self,others,selves):
        ps = [r for y in others for r in self.isectB(y)[0]]
        qs = [r for y in selves for r in self.isectB(y)[0]]
        return len(ps)%2 == len(qs)%2
