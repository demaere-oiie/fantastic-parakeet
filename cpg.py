from bezier import Bezier, Point
from svg import svgout

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

