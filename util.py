Eps = 1e-5

mid = lambda x,y: x + 0.5*(y-x)

close = lambda x,y: (y-x)**2<1e-2

def connect(xs):
    oxs = xs[:]
    ys, good = [],0
    if not xs: return xs
    pt = xs[0].b0
    z = pt
    while xs:
        for i,x in enumerate(xs):
            if pt.close(x.b0,1e3):
                ys.append(x)
                pt = x.b3
                xs = xs[:i]+xs[i+1:]
                if pt.close(z,1e3):
                    good = len(ys)+1
                    if len(xs):
                        pt = xs[0].b0
                        z = pt
                break
        else:
            for i,x in enumerate(xs):
                if pt.close(x.b3,1e3):
                    ys.append(x.flip())
                    pt = x.b0
                    xs = xs[:i]+xs[i+1:]
                    if pt.close(z,1e3):
                        good = len(ys)+1
                        if len(xs):
                            pt = xs[0].b0
                            z = pt
                    break
            else:
                print("!!!!!!")
                svgout3(ys)
                svgout3(oxs)
                return []
    return ys[:good]
