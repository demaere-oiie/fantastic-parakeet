from hershey import glyphs
from svg     import svgout2
from sys     import argv

gs = [glyphs(arg,5*i) for i,arg in enumerate(argv[1:])]
svgout2(sum([g.bs for g in gs],[]))
