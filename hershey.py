from bezier import Bezier
from point  import Point
from shape  import Shape
from stroke import shapesum, thickline
from topo   import connect

from pickle import dump, load
from svg    import svgout3

scale = 1/5.
cache = dict()

def setscale(x):
    global scale
    scale = x

def italic(s):
    def xform(p):
        return Point(p.x + 1 - 0.2*p.y, p.y)
    return Shape([Bezier(*map(xform,[b.b0,b.b1,b.b2,b.b3])) for b in s.bs])

def xhr(n):
    return (chr(n+32) if n<127-32 else
            chr(n-96+1040) if n<160 else
            chr(n-160+913) if n<177 else
            chr(n-160+914) if n<184 else
            chr(n-184+945) if n<201 else
            chr(n-184+946))

def debug(bs):
    svgout3(bs,dx=300,dy=800)

def glyph(x):
    c = x[0] if isinstance(x,tuple) else x
    style = ''.join(sorted(x[1])) if isinstance(x,tuple) else ""
    n = (ord(c)-32 if 32 <= ord(c) <= 126 else 
         ord(c)-913+160 if 913 <= ord(c) <= 930 else
         ord(c)-913+159 if 931 <= ord(c) <= 937 else
         ord(c)-945+184 if 945 <= ord(c) <= 961 else
         ord(c)-945+183 if 963 <= ord(c) <= 969 else
         ord(c)-1040+96 if 1040 <= ord(c) <= 1103 else
         127-32)
    if (n, style) not in cache:
      try:
        wid,pts = simplex[n]
        f = open(f"{n:03}{style}.p","rb")
      except:
        f = None
      if not f:
        print(f"render '{xhr(n)}' {style} {wid} {len(pts)}")
        ox, oy = -1,-1
        ls = []
        for x,y in zip(pts[0::2],pts[1::2]):
            draw = (x != -1 or y != -1)
            nx =     100*scale*x if draw else -1
            ny = 500-100*scale*y if draw else -1
            if ox != -1 and oy != -1 and nx != -1 and ny != -1:
                ls.append(thickline(Point(ox,oy),Point(nx,ny),
                                    1.5 if "b" in style else 1,
                                    nib=("n" in style)))
            ox,oy = nx,ny
        ss =([] if "s" not in style else
             thickline(Point(0,2500*scale),Point(wid*100*scale,2500*scale),1))
        s = (Shape( # debug(shapesum([Shape(l) for l in ls]).bs) or
                   connect(shapesum([Shape(l) for l in ls]).bs+ss) or
                   connect(shapesum([Shape(l) for l in ls[::-1]]).bs+ss or
                   [])).watertight().scale(.01))
        f = open(f"{n:03}{style}.p","wb")
        dump(s,f)
        f.close()
      else:
        s = load(f)
        f.close()
      cache[(n,style)] = (wid*scale,s if "i" not in style else italic(s))
    return cache[(n,style)]

def width(s):
    cton = lambda c: ord(c)-32 if 32<=ord(c)<=126 else 127-32
    return sum(simplex[cton(c)][0] for c in s)*scale

def glyphs(s,y=0,wid=0,align="left"):
    gs = [glyph(c) for c in s]
    extra = wid - sum(w for w,s in gs) if wid else 0
    nspace = sum(len(s.bs)==0 for w,s in gs)
    if align=="full":
      gs2 = [(w if len(s.bs) else w+extra/nspace,s) for w,s in gs]
    elif align=="center":
      gs2 = [(extra/2,Shape([]))]+gs
    elif align=="right":
      gs2 = [(extra,Shape([]))]+gs
    else:
      gs2 = gs
    return Shape([b for i,(w,s) in enumerate(gs2)
                    for b in s.translate(sum(w for w,s in gs2[:i]),y).bs])

xange = lambda l,h: list(range(l,h))
puncs = (      [0x109,0x10C,0x11C,0x10E,921,0x11D,282] +
         [0x110,0x111,869,0x114,0x106,0x113,0x105,0x10F] +
         xange(0x0FB,0x103)+
         [0x103,0x104,0x107,0x108,891,0x115,892,0x10A] +
         [923])
puncs2 = [0x29D,0x144,0x29E,912,0x18F,281]
puncs3 = [0x29F,274,0x2A0,896,964]
cyr    = xange(1171,1171+1103-1040+1)
ell    = xange(115,139)+xange(192,217)
F =\
{"serif"   : puncs+xange(0x4D3,0x4ED)+puncs2+xange(0x507,0x521)+puncs3+cyr
,"fraktur" : puncs+xange(0x57D,0x597)+puncs2+xange(0x597,0x5B1)+puncs3+cyr
,"italic"  : puncs+xange(0x2D7,0x2F1)+puncs2+xange(0x324,0x33E)+puncs3+cyr
,"simplex" : puncs+xange(0x059,0x073)+puncs2+xange(0x0A6,0x0C0)+puncs3+cyr+ell
,"sample"  : xange(4*95,5*95)
,"medieval": puncs+xange(1545,1571)+puncs2+xange(1571,1597)+puncs3
}

def cvt(s,o):
     return [r
        for l,h in zip(s[0::2],s[1::2])
        for off in [lambda c: ord(c)-ord('R')]
        for r in ([-1,-1] if (l,h)==(' ','R') else
                  [off(l)-off(o),9-off(h)])]

def loadfont(f="simplex"):
     global simplex
     ls = open("hershey2").readlines()
     xlat = lambda s:[ord(s[9])-ord(s[8]),cvt(s[10:],s[8])]
     simplex = [[16,[]]]+[xlat(ls[i]) for i in F[f]]

loadfont("medieval")
