serno = 0

def writefile(s,pre="test"):
    global serno
    f = open(f"{pre}{serno}.svg","w")
    f.write(s)
    f.close()
    serno = serno + 1

def topath(bs):
    return f"M {bs[0].b0.x},{bs[0].b0.y} "+" ".join(
       f"C {b.b1.x},{b.b1.y} {b.b2.x},{b.b2.y} {b.b3.x},{b.b3.y}"
       for b in bs)

def topoints(b,ps):
    return " ".join(f"M{q.x},{q.y}h.001" for p in ps
               for q in [b.eval(p)])

def xeval(b,t):
    print((b,t))
    return eval(b,t)

def subbez(b,a,o):
    return b.split(o)[0].split(a/o)[1]

def toolap(c,os):
    return " ".join(f"M {b.b0.x},{b.b0.y} "+
        f"C {b.b1.x},{b.b1.y} {b.b2.x},{b.b2.y} {b.b3.x},{b.b3.y}"
        for o in os
        for b in [subbez(c,o[0],o[1])])

def svgout(bs,cs,xs):
    [isects,olaps] = xs
    s = f'''
<svg viewBox="-1 -1 12 12" xmlns="http://www.w3.org/2000/svg">
    <path stroke="blue" stroke-width="1.1" d="{topath(bs)}" fill="none" />
    <path stroke="green" d="{topath(cs)}" fill="none" />
    <path stroke="red" stroke-linecap="round" d="{topoints(bs[0],isects)}" />
    <path stroke="yellow" stroke-width="0.8" stroke-linecap="round" d="{toolap(bs[0],olaps)}" />
</svg>
    '''
    writefile(s)

def strokes(xs):
    s = ""
    while xs:
        p = xs[0].b0
        for j,x in enumerate(xs):
            if x.b3.close(p,1e3):
                s += f"M {p.x},{p.y} "+" ".join(
                     f"C {b.b1.x},{b.b1.y} {b.b2.x},{b.b2.y} {b.b3.x},{b.b3.y}"
                     for b in xs[:j+1])+"Z"
                xs = xs[j+1:]
                break
    return s

def svgout2(xs):
    writefile(f'''
<svg viewBox="-1 -1 12 12" xmlns="http://www.w3.org/2000/svg">
    <path stroke="blue" fill="#8080ff" d="{strokes(connect(xs))}" />
</svg>
    ''')

def strokes2(bs):
    return " ".join(f"M {b.b0.x},{b.b0.y} "+
        f"C {b.b1.x},{b.b1.y} {b.b2.x},{b.b2.y} {b.b3.x},{b.b3.y}"
        for b in bs)

def svgout3(xs,pre="test"):
    writefile(f'''
<svg viewBox="-1 -1 12 12" xmlns="http://www.w3.org/2000/svg">
    <path stroke="blue" stroke-width="0.1" fill="#8080ff" d="{strokes2(xs)}" />
</svg>
    ''',pre)

def trim(xs):
    while 1:
        ys = [x for x in xs if sum(x.b0.close(q) for y in xs for q in (y.b0,y.b3))>1 and sum(x.b3.close(q) for y in xs for q in (y.b0,y.b3))>1]
        if len(xs)==len(ys):
            break
        xs = ys[:]
    return ys

def connect(xs):
    #xs = trim(xs)
    if not(xs): return xs

    ys = connect1(xs)
    if not ys:
        xs = trim(xs)
        ys = connect1(xs)

    return xs

    yys = [(len(ys),ys[:]) for i in range(len(xs))
                   for ys in [connect1(xs[i:]+xs[:i])]]
    maxl = max(l for (l,ys) in yys)
    #print(len(xs), [l for l,y in yys])
    for l,ys in yys:
        if l == maxl:
            return ys

def connect1(xs,tol=1e3,dbg=False):
    #for i,x in enumerate(xs):
    #    print(i,x)
    oxs = xs[:]
    ys, good = [],0
    if not xs: return xs
    pt = xs[0].b0
    z = pt
    while xs:
        for i,x in enumerate(xs):
            if pt.close(x.b0,tol):
                if dbg: print("chain",i)
                ys.append(x)
                pt = x.b3
                xs = xs[:i]+xs[i+1:]
                if pt.close(z,tol):
                    if dbg: print("chain close")
                    good = len(ys)+1
                    if len(xs):
                        pt = xs[0].b0
                        z = pt
                break
        else:
            for i,x in enumerate(xs):
                if pt.close(x.b3,tol):
                    if dbg: print("flip",i)
                    # we need to reverse a bezier
                    ys.append(x.flip())
                    pt = x.b0
                    xs = xs[:i]+xs[i+1:]
                    if pt.close(z,tol):
                        if dbg: print("flip close")
                        good = len(ys)+1
                        if len(xs):
                            pt = xs[0].b0
                            z = pt
                    break
            else:
                if dbg: print("!!!")
                return []
                print("!!!!!!")
                svgout3(ys,"connect")
                svgout3(oxs,"connect")
                return []
    #print("-----")
    #for y in ys:
    #    print(y)
    return ys[:good]
