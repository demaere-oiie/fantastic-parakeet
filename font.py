from hershey import glyphs, setscale
from stroke  import setshrink
from svg     import svgout4
from sys     import argv

setscale(1/7.)
setshrink(3)

gs = [glyphs(arg,5*i,0) for i,arg in enumerate(argv[1:])]
svgout4([b for g in gs for b in g.scale(.1).bs])
