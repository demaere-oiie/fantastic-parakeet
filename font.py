from hershey import glyphs, setscale, width
from stroke  import setshrink
from svg     import svgout4
from sys     import argv

setscale(1/7.)
setshrink(3)

lorem = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit
in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui
officia deserunt mollit anim id est laborum.
""".split()

styles = ["","b","i","ib","s","sb","si","sib"][::-1]


def left(argv):
    gs = [glyphs(s,5*i,0) for i,s in enumerate(argv)]
    svgout4([b for g in gs
               for b in g.scale(.05).translate(2,2).bs])

def right(argv):
    gs = [glyphs(s,5*i,90,align="right") for i,s in enumerate(argv)]
    svgout4([b for g in gs
               for b in g.scale(.05).translate(2,2).bs])

def center(argv):
    gs = [glyphs(s,5*i,90,align="center") for i,s in enumerate(argv)]
    svgout4([b for g in gs
               for b in g.scale(.05).translate(2,2).bs])

def full(argv):
    gs = [glyphs(s,5*i,90,align="full") for i,s in enumerate(argv)]
    svgout4([b for g in gs
               for b in g.scale(.05).translate(2,2).bs])

def style(argv):
    ws = [(l,styles[i%8]) for i,l in enumerate(lorem[8:24])]
    gs = [glyphs([(c,z) for w,s in ws[i:i+4]
                    for c,z in [(c,s) for c in w]+[(" ","")]],5*(i//4),0)
              for i in range(0,len(ws),4)]
    svgout4([b for g in gs
               for b in g.scale(.05).translate(2,2).bs])

def flow(argv):
    WID = 75 if len(argv)<1 else int(argv[0])
    ws = lorem[:]
    gs = []
    while ws:
        i = 0
        while width(" ".join(ws[:i])) < WID and len(ws[i:]):
            i = i+1
        if width(" ".join(ws[:i])) > WID:
            i = i-1
        print(ws[:i])
        gs.append(glyphs(" ".join(w for w in ws[:i]),
                         5*len(gs), WID, align="full" if ws[i:] else "left"))
        ws = ws[i:]
    svgout4([b for g in gs
               for b in g.scale(.05).translate(2,2).bs])

def spiral(argv):
    gs = [(glyphs(s,5*i,0),width(s)) for i,s in enumerate(argv)]
    svgout4([b for g,w in gs for g1 in [g.scale(.05)]
               for b in g.translate(0,6).spiral().scale(.01).translate(6,6).bs])

cmds = {
"-l": left, "--left": left,
"-r": right, "--right": right,
"-c": center, "--center": center,
"-f": full, "--full": full,
"-y": style, "--style": style,
"-w": flow, "--flow": flow,
"-s": spiral, "--spiral": spiral,
}

if not argv[1].startswith("-"):
    argv = argv[:1]+["--left"]+argv[1:]

cmds.get(argv[1],left)(argv[2:])
