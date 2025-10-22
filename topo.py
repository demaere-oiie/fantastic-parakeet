from bezier import Bezier

def trim(xs):
    while 1:
        ys = [x for x in xs
            if sum(x.b0.near(q) for y in xs for q in (y.b0,y.b3))>1 and
               sum(x.b3.near(q) for y in xs for q in (y.b0,y.b3))>1 ]
        if len(xs)==len(ys):
            break
        xs = ys[:]
    return ys

def connect(xs):
    return xs and (connect1(xs) or connect1(trim(xs),dbg=True))

def connect1(xs,tol=1e3,dbg=False):
    oxs = xs[:]
    ys, good = [],0
    if not xs: return xs
    pt = xs[0].b0
    z = pt
    while xs:
        for i,x in enumerate(xs):
            if pt.near(x.b0,tol):
                ys.append(x)
                pt = x.b3
                xs = xs[:i]+xs[i+1:]
                if pt.near(z,tol):
                    good = len(ys)+1
                    if len(xs):
                        pt = xs[0].b0
                        z = pt
                break
        else:
            for i,x in enumerate(xs):
                if pt.near(x.b3,tol):
                    # we need to reverse a bezier
                    ys.append(Bezier(x.b3,x.b2,x.b1,x.b0))
                    pt = x.b0
                    xs = xs[:i]+xs[i+1:]
                    if pt.near(z,tol):
                        good = len(ys)+1
                        if len(xs):
                            pt = xs[0].b0
                            z = pt
                    break
            else:
                if dbg: print("!!!")
                return []
    return ys[:good]
