def xor1d(bs,cs):
    ds = sorted(bs + cs)
    return [d for i,d in enumerate(ds)
              if not any((c-d)**2<1e-6 for c in ds[:i]+ds[i+1:])]

def merge(xs):
    # it's wrong, but for now assume at most one overlap
    ta, to = 1.0, 0.0
    for b1,b2,xta,xto,xua,xuo,xx in xs:
        ta = min(ta,(xta+xto)/2)
        to = max(to,(xta+xto)/2)
    return [(ta,to)]

kludge = 1500

def isect_raw(xs, a, b, n):
    if len(xs) > kludge:
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

mid = lambda x,y: x + 0.5*(y-x)

Eps = 1e-5
