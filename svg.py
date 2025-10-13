serno = 0

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
    global serno
    [isects,olaps] = xs
    s = f'''
<svg viewBox="-1 -1 12 12" xmlns="http://www.w3.org/2000/svg">
    <path stroke="blue" stroke-width="1.1" d="{topath(bs)}" fill="none" />
    <path stroke="green" d="{topath(cs)}" fill="none" />
    <path stroke="red" stroke-linecap="round" d="{topoints(bs[0],isects)}" />
    <path stroke="yellow" stroke-width="0.8" stroke-linecap="round" d="{toolap(bs[0],olaps)}" />
</svg>
    '''
    f = open(f"test{serno}.svg","w")
    f.write(s)
    f.close()
    serno = serno + 1

def connect(xs):
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
                for y in ys:
                    print(y)
                print("!!!",pt)
                for x in xs:
                    print(x)
                [][0]
    return ys[:good]

def strokes(xs):
    return f"M {xs[0].b0.x},{xs[0].b0.y} "+" ".join(
        f"C {b.b1.x},{b.b1.y} {b.b2.x},{b.b2.y} {b.b3.x},{b.b3.y}"
        for b in xs)+"Z" if xs else ""

def svgout2(xs):
    global serno
    s = f'''
<svg viewBox="-1 -1 12 12" xmlns="http://www.w3.org/2000/svg">
    <path stroke="blue" fill="#8080ff" d="{strokes(connect(xs))}" />
</svg>
    '''
    f = open(f"test{serno}.svg","w")
    f.write(s)
    f.close()
    serno = serno + 1

def strokes2(bs):
    return " ".join(f"M {b.b0.x},{b.b0.y} "+
        f"C {b.b1.x},{b.b1.y} {b.b2.x},{b.b2.y} {b.b3.x},{b.b3.y}"
        for b in bs)

def svgout3(xs):
    global serno
    s = f'''
<svg viewBox="-1 -1 12 12" xmlns="http://www.w3.org/2000/svg">
    <path stroke="blue" stroke-width="0.1" fill="#8080ff" d="{strokes2(xs)}" />
</svg>
    '''
    f = open(f"test{serno}.svg","w")
    f.write(s)
    f.close()
    serno = serno + 1
