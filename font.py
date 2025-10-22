from point   import Point
from stroke  import thickpoly
from svg     import svgout2, svgout3

#svgout2(thickpoly([Point(1,1),Point(1,5),Point(5,5),Point(5,1)]).bs)

from hershey import glyphs

svgout2(glyphs('we do this').bs)
svgout2(glyphs('not because').bs)
svgout2(glyphs('it is easy').bs)
