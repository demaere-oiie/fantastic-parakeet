from hershey import glyphs, setscale
from stroke  import setshrink
from svg     import svgout4
from sys     import argv

setscale(1/7.)
setshrink(3)

lorem = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
""".split()

styles = ["","b","i","ib","s","sb","si","sib"]

ws = [(l,styles[i%8]) for i,l in enumerate(lorem[:8])]
gs = [glyphs([(c,s) for w,s in ws[i:i+2]+[(" ","")] for c in w],5*(i//2),0)
      for i in range(0,len(ws),2)]
svgout4([b for g in gs for b in g.scale(.05).bs])
