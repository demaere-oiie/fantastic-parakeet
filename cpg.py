from bezier import Bezier, Point
from shape import Shape
from svg import svgout, svgout2, svgout3

def B(*ps):
    return Bezier(*[Point(*p) for p in ps])

shapes = [Shape(bs) for bs in [
    [B((0,0),(1,0),(0,8),(8,8)),
     B((8,8),(7,8),(8,0),(0,0))],
    [B((0,8),(1,8),(0,0),(8,0)),
     B((8,0),(7,0),(8,8),(0,8))],
    [B((0,0),(1,0),(7,0),(8,0)),
     B((8,0),(8,8),(0,8),(0,0))],
    [B((2,0),(3,0),(5,0),(6,0)),
     B((6,0),(6,6),(2,6),(2,0))],
    [B((4,0),(4,1),(4,5),(4,6)),
     B((4,6),(0,6),(0,0),(4,0))],
    [B((4,4),(4,5),(4,7),(4,8)),
     B((4,8),(8,8),(8,4),(4,4))],
    [B((0,0),(1,0),(7,0),(8,0)),
     B((8,0),(8,1),(5,4),(4,4)),
     B((4,4),(3,4),(0,1),(0,0))],
    [B((2,0),(3,0),(5,0),(6,0)),
     B((6,0),(6,1),(5,3),(4,3)),
     B((4,3),(3,3),(2,1),(2,0))],
]]

if __name__=="__main__":
    import sys

    if 0:
      for i,s in enumerate(shapes):
        print("#",i)
        if not s.beq(s):
            print("a != a: ",s)

        if not s.bor(Shape([])).beq(s):
            print("a | 0 != a: ",s)

        if not s.bor(s).beq(s):
            print("a | a != a: ",s)

        if not s.band(s).beq(s):
            print("a & a != a: ",s)

    if 0:
      for i,s in enumerate(shapes):
        for j,t in enumerate(shapes[:i+1]):
            print("#",i,j)
            u = s.band(t)
            v = s.bor(t)
            if u.beq(s) and not v.beq(t):
                    print("!!!",s,t)
            if u.beq(t) and not v.beq(s):
                    print("!!!",s,t)

            if not u.beq(t.band(s)):
                    print("===",s,t)

            if not v.beq(t.bor(s)):
                    print("===",s,t)

            if not u.ble(s):
                    print("!!!",u,s,t)
            if not u.ble(t):
                    print("!!!",u,s,t)

            if not s.ble(v):
                print("!!!",v,s,t)
            if not t.ble(v):
                print("!!!",v,s,t)

            if not s.bxor(t).ble(v):
                print("s^t<=s|t",v,s,t)

            if not u.ble(v):
                print("s&t<=s|t",v,s,t)

    if 1:
      for i,s in enumerate(shapes):
        for j,t in enumerate(shapes[:i+1]):
            for k,u in enumerate(shapes[:j+1]):

                print("#",i,j,k)
                v = s.band(t.bxor(u))
                w = (s.band(t)).bxor(s.band(u))
                if not v.beq(w):
                    print("s&(t^u) == (s^t)&(s^u)",s,t,u)
