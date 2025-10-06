from bezier import Bezier, Point
from shape import Shape
from svg import svgout, svgout2

def B(*ps):
    return Bezier(*[Point(*p) for p in ps])

if __name__=="__main__":
    a = B((1,1),(6,1),(8,2),(8,8))
    b = B((1,8),(6,2),(8,1),(8,1))
    print(a.isect(b))
    svgout([a],[b],a.isect(b))
    a = B((0,0),(32,0),(-24,8),(8,8))
    b = B((0,8),(0,-24),(8,32),(8,0))
    print(a.isect(b))
    svgout([a],[b],a.isect(b))
    a = B((0,0),(1,1),(7,7),(8,8))
    b = B((1,0),(2,1),(8,7),(9,8))
    print(a.isect(b))
    svgout([a],[b],a.isect(b))
    a = B((1,1),(6,1),(8,2),(8,8))
    b = B((8,8),(8,2),(6,1),(1,1))
    print(a.isect(b))
    a = B((1,1),(6,1),(8,2),(8,8))
    b = B((8,8),(8,2),(6,1),(1,1))
    print(a.isect(b))
    a = B((0,0),(1,1),(7,7),(8,8))
    b = B((4,4),(5,5),(11,11),(12,12))
    print(a.isect(b))
    svgout([a],[b],a.isect(b))
    a = B((1,1),(6,1),(8,2),(8,8))
    b = B((8,8),(8,2),(6,1),(1,1))
    print(a.covered([b])) # reparamaterization
    a = B((1,1),(6,1),(8,2),(8,8))
    b = B((1,8),(6,2),(8,1),(8,1))
    print(a.covered([b])==False) # not a bcover
    a = B((0,0),(1,1),(7,7),(8,8))
    bs = [B((0,0),(1,1),(3,3),(4,4)),B((4,4),(5,5),(7,7),(8,8))]
    print(a.covered(bs)) # not 1:1
    a = B((0,0),(1,1),(7,7),(8,8))
    bs = [B((-1,-1),(1,1),(3,3),(4,4)),B((4,4),(5,5),(7,7),(9,9))]
    print(a.covered(bs)) # not 1:1, not at endpoints
    a = B((0,0),(0,1),(0,7),(0,8))
    a0,a1 = a.split(0.7)
    b = B((0,0),(1,0),(7,0),(8,0))
    b0,b1 = b.split(0.3)
    c = B((0,8),(1,7),(7,1),(8,0))
    print(Shape([a,b0,b1,c]).beq(Shape([c,a0,a1,b])))
    a = B((0,0),(0,1),(0,7),(0,8))
    b = B((0,0),(1,0),(7,0),(8,0))
    c = B((0,8),(4,8),(4,0),(8,0))
    c0,c1 = c.split(0.3)
    c2,c3 = c.split(0.7)
    d = B((0,8),(1,8),(7,8),(8,8))
    e = B((8,0),(8,1),(8,7),(8,8))
    svgout2(Shape([a,b,c0,c1]).bxor(Shape([c2,c3,d,e])).bs)
    svgout2([a,b,c0,c1])
    svgout2([c2,c3,d,e])
    a = B((0,0),(1,0),(0,8),(8,8))
    b = B((8,8),(7,8),(8,0),(0,0))
    c = B((0,8),(1,8),(0,0),(8,0))
    d = B((8,0),(7,0),(8,8),(0,8))
    svgout2([a,b])
    svgout2([c,d])
    svgout2(Shape([a,b]).band(Shape([c,d])).bs)

