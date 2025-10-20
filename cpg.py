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

only = {}
excl = {}

if __name__=="__main__":
    import sys

    if 0:
      for i,s in enumerate(shapes):
        print("#",i)

        if only and (i,) not in only: continue

        if not s.beq(s):
            print("a == a: ",s)

        if not s.bor(Shape([])).beq(s):
            print("a | 0 == a: ",s)

        if not s.bor(s).beq(s):
            print("a | a == a: ",s)

        if not s.band(s).beq(s):
            print("a & a == a: ",s)
 
    if 0:
      for i,s in enumerate(shapes):
        for j,t in enumerate(shapes[:i+1]):
            print("#",i,j)

            if only and (i,j) not in only: continue
            if excl and (i,j) in excl: continue

            u = s.band(t)
            v = s.bor(t)

            if not u.beq(t.band(s)):
                print("s&t == t&s",s,t)

            if not v.beq(t.bor(s)):
                print("s|t == t|s",s,t)

            if not s.bxor(t).bxor(s).beq(t):
                print("(s^t)^s == t",s,t)

            if not u.ble(s):
                print("s&t <= s",u,s,t)
            if not u.ble(t):
                print("s&t <= t",u,s,t)

            if not s.ble(v):
                print("s <= s|t",v,s,t)
            if not t.ble(v):
                print("t <= s|t",v,s,t)
                svgout3(t.bs)
                svgout3(v.bs)
                svgout3(t.bs+v.bs)
                svgout3(t.bxor(v.band(t)).bs)
                sys.exit(0)

            if not s.bxor(t).ble(v):
                print("s^t<=s|t",v,s,t)
                w = s.bxor(t)
                svgout3(w.bs)
                svgout3(v.bs)
                svgout3(v.db_and(w).bs)
                svgout3(w.bxor(v.band(w)).bs)
                sys.exit(0)

            if not u.ble(v):
                print("s&t <= s|t",v,s,t)

            if not u.bor(t).beq(t):
                print("(s&t)|t==t",s,t)
                print(v.band(t).bxor(t).bs)
                sys.exit(0)

            if not v.band(t).beq(t):
                print("(s|t)&t==t",s,t)
                svgout3(v.bs)
                svgout3(v.db_and(t).bs)
                svgout3(t.bs)
                print(v.band(t).bxor(t).bs)
                sys.exit(0)

    if 1:
      for i,s in enumerate(shapes):
        for j,t in enumerate(shapes[:i+1]):
            for k,u in enumerate(shapes[:j+1]):

                print("#",i,j,k)

                if only and (i,j,k) not in only: continue

                v = s.band(t.bor(u))
                w = (s.band(t)).bor(s.band(u))
                if not v.beq(w):
                    print("s&(t|u) == (s&t)|(s&u)",s,t,u)
                    svgout3(v.bs)
                    svgout3(w.bs)
                    svgout3(v.bxor(w).bs)
                    svgout3(s.bs+t.bs+u.bs)
                    sys.exit(0)

                v = s.band(t.bxor(u))
                w = (s.band(t)).bxor(s.band(u))
                if not v.beq(w):
                    print("s&(t^u) == (s&t)^(s&u)",s,t,u)

                v = s.band(t.band(u))
                w = s.band(t).band(u)
                if not v.beq(w):
                    print("(s&t)&u == s&(t&u)",s,t,u)
                    svgout3(v.bs)
                    svgout3(w.bs)
                    svgout3(s.bs+t.bs+u.bs)
                    svgout3(s.bs)
                    svgout3(t.band(u).bs)
                    s.db_and(t.band(u))
                    sys.exit(0)

                v = s.bxor(t.bxor(u))
                w = s.bxor(t).bxor(u)
                if not v.beq(w):
                    print("(s^t)^u == s^(t^u)",s,t,u)
