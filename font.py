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

#ws = [(l,styles[i%8]) for i,l in enumerate(lorem[8:24])]
#gs = [glyphs([(c,z) for w,s in ws[i:i+4]
#                    for c,z in [(c,s) for c in w]+[(" ","")]],5*(i//4),0)
#      for i in range(0,len(ws),4)]

WID = 60 if len(argv)<2 else int(argv[1])
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
svgout4([b for g in gs for b in g.scale(.05).bs])
