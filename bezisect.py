_=min

Eps = 1e-5

mid = lambda x,y: x+0.5*(y-x)

split = lambda b,t: _([(p0,q0,r0,s),(s,r1,q2,p3)]
    for med in [lambda t,p,q: _((px+t*(qx-px),py+t*(qy-py))
         for px,py in [p] for qx,qy in [q])]
    for p0,p1,p2,p3 in [b]
    for q0 in [med(t,p0,p1)]
    for q1 in [med(t,p1,p2)]
    for q2 in [med(t,p2,p3)]
    for r0 in [med(t,q0,q1)]
    for r1 in [med(t,q1,q2)]
    for s  in [med(t,r0,r1)])

bbox = lambda b: (min(x for x,y in b), min(y for x,y in b),
                  max(x for x,y in b), max(y for x,y in b))

close = lambda p,q,s=2: abs(p[0]-q[0])<s*Eps and abs(p[1]-q[1])<s*Eps

################################################################################

def eval(a,t):
    [b,c] = split(a,t)
    return b[-1]

def isect(a,b):
    xs,ms = isect1([(a,b,0.,1.,0.,1.,'d')],a,b,0)
    ys = []
    for b1,b2,ta,to,ua,uo,xx in xs:
        if xx=='x':
            t = mid(ta,to)
            u = mid(ua,uo)
            (x,y) = eval(a,t)
            if not any(close(p,(x,y)) for p in ys):
                ys.append((x,y))
    return (ys,ms)

def merge(xs):
    # it's wrong, but for now assume at most one overlap
    ta, to = 1.0, 0.0
    ua, uo = 1.0, 0.0
    for b1,b2,xta,xto,xua,xuo,xx in sorted(xs):
        ta = min(ta,xta)
        to = max(to,xto)
        ua = min(ua,xua)
        uo = max(uo,xuo)

    return [(ta,to,ua,uo)]

def isect1(xs, a, b, n):
    if len(xs) > 1000: #45:
        return (xs, merge(xs))
    else:
        ys = [r
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
            for bb1 in [bbox(b1)]
            for bb2 in [bbox(b2)]
          for st,su in [(0.5,0.5)]
          for b11,b12 in [split(b1,st)]
          for b21,b22 in [split(b2,su)]
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
    return isect1(ys, a, b, n+1)

################################################################################

def xor(bs,cs):
    ds = sorted(bs + cs)
    return [d for i,d in enumerate(ds)
              if not any((c-d)**2<1e-2 for c in ds[:i]+ds[i+1:])]

def bcovers(bs,cs):
    for b in bs:
        olap = [0.,1.]
        for c in cs:
            ys,ms = isect(b,c)
            olap = xor(olap,[r for m in ms for r in m[:2]])
        if olap:
            return False
    return True

################################################################################

serno = 0

def topath(bs):
    return f"M {bs[0][0][0]},{bs[0][0][1]} "+" ".join(
       f"C {b[1][0]},{b[1][1]} {b[2][0]},{b[2][1]} {b[3][0]},{b[3][1]}"
       for b in bs)

def topoints(ps):
    return " ".join(f"M {p[0]},{p[1]} h .001" for p in ps)

def xeval(b,t):
    print((b,t))
    return eval(b,t)

def subbez(b,a,o):
    return split(split(b,o)[0],a/o)[1]

def toolap(c,os):
    return " ".join(f"M {b[0][0]},{b[0][1]} "+
        f"C {b[1][0]},{b[1][1]} {b[2][0]},{b[2][1]} {b[3][0]},{b[3][1]}"
        for o in os
        for b in [subbez(c,o[0],o[1])])

def svgout(bs,cs,xs):
    global serno
    [isects,olaps] = xs
    s = f'''
<svg viewBox="-1 -1 12 12" xmlns="http://www.w3.org/2000/svg">
    <path stroke="blue" stroke-width="1.1" d="{topath(bs)}" fill="none" />
    <path stroke="green" d="{topath(cs)}" fill="none" />
    <path stroke="red" stroke-linecap="round" d="{topoints(isects)}" />
    <path stroke="yellow" stroke-width="0.8" stroke-linecap="round" d="{toolap(bs[0],olaps)}" />
</svg>
    '''
    f = open(f"test{serno}.svg","w")
    f.write(s)
    f.close()
    serno = serno + 1

################################################################################

def shape_eq(x,y):
    return bcovers(x,y) and bcovers(y,x)

################################################################################

if __name__=="__main__":
    a = ((1,1),(6,1),(8,2),(8,8))
    b = ((1,8),(6,2),(8,1),(8,1))
    print(isect(a,b))
    svgout([a],[b],isect(a,b))
    a = ((0,0),(32,0),(-24,8),(8,8))
    b = ((0,8),(0,-24),(8,32),(8,0))
    print(isect(a,b))
    svgout([a],[b],isect(a,b))
    a = ((0,0),(1,1),(7,7),(8,8))
    b = ((1,0),(2,1),(8,7),(9,8))
    print(isect(a,b))
    svgout([a],[b],isect(a,b))
    a = ((1,1),(6,1),(8,2),(8,8))
    b = ((8,8),(8,2),(6,1),(1,1))
    print(isect(a,b))
    a = ((1,1),(6,1),(8,2),(8,8))
    b = ((8,8),(8,2),(6,1),(1,1))
    print(isect(a,b))
    a = ((0,0),(1,1),(7,7),(8,8))
    b = ((4,4),(5,5),(11,11),(12,12))
    print(isect(a,b))
    svgout([a],[b],isect(a,b))
    a = ((1,1),(6,1),(8,2),(8,8))
    b = ((8,8),(8,2),(6,1),(1,1))
    print(bcovers([a],[b])) # reparamaterization
    a = ((1,1),(6,1),(8,2),(8,8))
    b = ((1,8),(6,2),(8,1),(8,1))
    print(bcovers([a],[b])) # not a bcover
    a = ((0,0),(1,1),(7,7),(8,8))
    bs = [((0,0),(1,1),(3,3),(4,4)),((4,4),(5,5),(7,7),(8,8))]
    print(bcovers([a],bs)) # not 1:1
    a = ((0,0),(1,1),(7,7),(8,8))
    bs = [((-1,-1),(1,1),(3,3),(4,4)),((4,4),(5,5),(7,7),(9,9))]
    print(bcovers([a],bs)) # not 1:1, not at endpoints
    a = ((0,0),(0,1),(0,7),(0,8))
    a0,a1 = split(a,0.7)
    b = ((0,0),(1,0),(7,0),(8,0))
    b0,b1 = split(b,0.3)
    c = ((0,8),(1,7),(7,1),(8,0))
    print(shape_eq([a,b0,b1,c],[c,a0,a1,b]))
