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

def strokes2(bs):
    return " ".join(f"M {b.b0.x},{b.b0.y} "+
        f"C {b.b1.x},{b.b1.y} {b.b2.x},{b.b2.y} {b.b3.x},{b.b3.y}"
        for b in bs)

def dump(ys,xs):
    print(f'''
<svg viewBox="-1 -1 12 12" xmlns="http://www.w3.org/2000/svg">
    <path stroke="red" stroke-width="0.1" fill="#8080ff" d="{strokes2(ys)}" />
    <path stroke="blue" stroke-width="0.1" fill="#8080ff" d="{strokes2(xs)}" />
</svg>
    ''')

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
                dump(ys[good:],xs)
                tol = tol*10
                print("!!!",len(xs),tol)
                if tol>1e5:
                    if dbg==False: return []
                    ys = ys[:good]
                    tol = 1e3
                    pt = xs[0].b0
                    z = pt
    return ys[:good]
