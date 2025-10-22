from point   import Point
from stroke  import thickpoly
from svg     import svgout2, svgout3

svgout2(thickpoly([Point(1,1),Point(1,5),Point(5,5),Point(5,1)]).bs)
