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

def isect(a,b):
    return isect1([(a,b,0.,1.,0.,1.,'d')],a,b,0)

def merge(xs):
    print("**** merge ****")
    return xs

def isect1(xs, a, b, n):
    if len(xs) > 30:
        ys = merge(xs)
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
        return xs
    return isect1(ys, a, b, n+1)

################################################################################

if __name__=="__main__":
    a = ((1,1),(6,1),(8,2),(8,8))
    # b = ((1,8),(6,2),(8,1),(8,1))
    b = ((0,8),(5,2),(7,1),(7,1))
    for x in isect(a,b):
        print(x)
