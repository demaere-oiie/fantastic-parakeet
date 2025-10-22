from bezier import Bezier
from point import Point
from shape import Shape

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

    if 1:
      Zero = Shape([])
      One = Shape([B((-.5,-.5),(9,-.5),(-.5,-.5),(9,-.5)),
                   B((9,-.5),(9,9),(9,-.5),(9,9)),
                   B((9,9),(-.5,9),(9,9),(-.5,9)),
                   B((-.5,9),(-.5,-.5),(-.5,9),(-.5,-.5))])
      for i,s in enumerate(shapes):
        print("#",i)

        if only and (i,) not in only: continue

        if not s.beq(s):
            print("a == a: ",s)

        if not s.bxor(Zero).beq(s):
            print("a ^ 0 == a: ", s)

        if not s.band(Zero).beq(Zero):
            print("a & 0 == 0: ", s)

        if not s.bor(Zero).beq(s):
            print("a | 0 == a: ",s)

        if not s.bxor(s).beq(Zero):
            print("a ^ a == 0: ",s)

        if not s.band(s).beq(s):
            print("a & a == a: ",s)

        if not s.bor(s).beq(s):
            print("a | a == a: ",s)

        if not s.band(One).beq(s):
            print("a & 1 == a: ",s)
 
    if 1:
      for i,s in enumerate(shapes):
        for j,t in enumerate(shapes[:i+1]):
            print("#",i,j)

            if only and (i,j) not in only: continue
            if excl and (i,j) in excl: continue

            u = s.band(t)
            v = s.bor(t)
            w = s.bxor(t)
            
            if not u.beq(t.band(s)):
                print("s&t == t&s",s,t)

            if not w.beq(t.bxor(s)):
                print("s^t == t^s",s,t)

            if not v.beq(t.bor(s)):
                print("s|t == t|s",s,t)

            if not w.bxor(s).beq(t):
                print("(s^t)^s == t",s,t)

            if not u.ble(s):
                print("s&t <= s",u,s,t)
            if not u.ble(t):
                print("s&t <= t",u,s,t)

            if not s.ble(v):
                print("s <= s|t",v,s,t)
            if not t.ble(v):
                print("t <= s|t",v,s,t)

            if not w.ble(v):
                print("s^t <= s|t",v,s,t)
            if not u.ble(v):
                print("s&t <= s|t",v,s,t)

            if not u.bor(t).beq(t):
                print("(s&t)|t==t",s,t)

            if not v.band(t).beq(t):
                print("(s|t)&t==t",s,t)

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

                v = s.band(t.bxor(u))
                w = (s.band(t)).bxor(s.band(u))
                if not v.beq(w):
                    print("s&(t^u) == (s&t)^(s&u)",s,t,u)

                v = s.band(t.band(u))
                w = s.band(t).band(u)
                if not v.beq(w):
                    print("(s&t)&u == s&(t&u)",s,t,u)

                v = s.bxor(t.bxor(u))
                w = s.bxor(t).bxor(u)
                if not v.beq(w):
                    print("(s^t)^u == s^(t^u)",s,t,u)

                v = s.bor(t.bor(u))
                w = s.bor(t).bor(u)
                if not v.beq(w):
                    print("(s|t)|u == s|(t|u)",s,t,u)
