from bezier import Bezier
from point  import Point
from shape  import Shape
from svg    import svgout3

shrink = 3

def setshrink(x):
    global shrink
    shrink = x

def line(p,q):
    return [Bezier(p,p.lerp(q,0.33),q.lerp(p,0.33),q)]

def poly(ps):
    return sum([line(a,b) for a,b in zip(ps,ps[1:]+ps[:1])],[])

def norm(x,y): return (x**2 + y**2)**0.5
def abs(v):    return -v if v<0 else v

def thickline(p,q,w,nib=False):
    dx, dy = (q.x-p.x, q.y-p.y)
    scale  = shrink*norm(dx,dy)
    unx, uny = -dy/scale*w, dx/scale*w
    if nib:
        unx += 1.2*unx*abs(0.707*unx - 0.707*uny)/norm(unx,uny)
        uny += 1.2*uny*abs(0.707*unx - 0.707*uny)/norm(unx,uny)
    c = 1.3
    return (line(Point(p.x+unx,p.y+uny), Point(q.x+unx,q.y+uny)) +
        [Bezier(Point(q.x+unx,q.y+uny),Point(q.x+unx+c*uny,q.y+uny+c*(-unx)),
                Point(q.x-unx+c*uny,q.y-uny+c*(-unx)),Point(q.x-unx,q.y-uny))]+
            line(Point(q.x-unx,q.y-uny), Point(p.x-unx,p.y-uny)) +
        [Bezier(Point(p.x-unx,p.y-uny),Point(p.x-unx+c*(-uny),p.y-uny+c*unx),
                Point(p.x+unx+c*(-uny),p.y+uny+c*unx),Point(p.x+unx,p.y+uny))])

def shapesum(ss):
    zero = Shape([])
    if not len(ss):
        return zero
    elif len(ss)==1:
        return ss[0]
    else:
        return shapesum([x.bor(y) for x,y in zip(ss[0::2],ss[1::2]+[zero])])

def thickpoly(ps):
    return shapesum([Shape(thickline(p,q)) for p,q in zip(ps[:-1],ps[1:])])
