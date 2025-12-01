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

def strokes(xs,n=1e3):
    s = ""
    z = 0
    for i,x in enumerate(xs):
        if i==z: s+= f"M {x.b0.x},{x.b0.y} "
        s += f"C {x.b1.x},{x.b1.y} {x.b2.x},{x.b2.y} {x.b3.x},{x.b3.y}"
        if x.b3.near(xs[z].b0,1):
            s += "Z"
            z = i+1
    #assert z==len(xs)
    return s

def svgout2(xs, width=0.1):
    writefile(f'''
<svg viewBox="-1 -1 12 12" xmlns="http://www.w3.org/2000/svg">
    <path stroke-width="{width}" stroke="blue" fill="#8080ff" d="{strokes(xs)}" />
</svg>
    ''')

def strokes2(bs):
    return " ".join(f"M {b.b0.x},{b.b0.y} "+
        f"C {b.b1.x},{b.b1.y} {b.b2.x},{b.b2.y} {b.b3.x},{b.b3.y}"
        for b in bs)

def svgout3(xs,pre="test",dx=12,dy=12):
    writefile(f'''
<svg viewBox="-1 -1 {dx} {dy}" xmlns="http://www.w3.org/2000/svg">
    <path stroke="blue" stroke-width="0.1" fill="#8080ff" d="{strokes2(xs)}" />
</svg>
    ''',pre)

def svgout4(xs):
    writefile(f'''
<svg viewBox="-1 -1 12 12" xmlns="http://www.w3.org/2000/svg">
    <path stroke-width="0" stroke="blue" fill="black" d="{strokes(xs,1e2)}" />
</svg>
    ''')

def svgout5(xs):
    writefile(f'''
<svg viewBox="-1 -1 300 600" xmlns="http://www.w3.org/2000/svg">
    <path stroke="blue" stroke-width="0.1" fill="#8080ff" d="{strokes2(xs)}" />
    <path stroke="green" stroke-width="5" fill="#8080ff" d="M {xs[0].b0.x},{xs[0].b0.y} h 5" />
    <path stroke="red" stroke-width="5" fill="#8080ff" d="M {xs[-1].b3.x},{xs[-1].b3.y} h 5" />
</svg>
    ''')
