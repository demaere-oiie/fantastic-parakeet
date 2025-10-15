Eps = 1e-5

mid = lambda x,y: x + 0.5*(y-x)

close = lambda x,y: (y-x)**2<1e-2

def connect(xs):
    #for i,x in enumerate(xs):
    #    print(i,x)
    oxs = xs[:]
    ys, good = [],0
    if not xs: return xs
    pt = xs[0].b0
    z = pt
    while xs:
        for i,x in enumerate(xs):
            if pt.close(x.b0,1e3):
                #print("chain",i)
                ys.append(x)
                pt = x.b3
                xs = xs[:i]+xs[i+1:]
                if pt.close(z,1e3):
                    #print("chain close")
                    good = len(ys)+1
                    if len(xs):
                        pt = xs[0].b0
                        z = pt
                break
        else:
          for j,y in enumerate(ys):
            if pt.close(y.b0,1e3):
                #print("tail",j)
                # we have a tail before our good loop
                xs = xs+ys[good+1:j]
                ys = ys[:good]+ys[j:]
                good = len(ys)+1
                if len(xs):
                    #print("tail close")
                    pt = xs[0].b0
                    z = pt
                break
          else:
            for i,x in enumerate(xs):
                if pt.close(x.b3,1e3):
                    #print("flip",i)
                    # we need to reverse a bezier
                    ys.append(x.flip())
                    pt = x.b0
                    xs = xs[:i]+xs[i+1:]
                    if pt.close(z,1e3):
                        #print("flip close")
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
    #print("-----")
    #for y in ys:
    #    print(y)
    return ys[:good]
