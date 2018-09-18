#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module : calculations.py
Website: https://github.com/ruminations/Geyser
License: https://github.com/ruminations/Licenses#design-license
Initial Copyright August 2018

This is a collection of python fragments that automate some of the more
complex calculations involved in generating the .scad and .svg files for
depicting the design of the Geyser extruder assembly.

Implementaion notes:

Following typical python convention, a single '_' prefix denotes an object
that is essentially 'private' - it is either a detail that normally a user
is unconcerned with, or the interface is awkward, tailored to an internal
purpose.

The '__slots__' idiom is used pervasively.  This is not 'java-style'.  It
is 'cython-style'.  Cython is, in essence, a civilized C-language, and the
'__slots__' idiom sketches in variable declaration that would ultimately
be implemented in cython.  I habitually write in this style because much
of what I write ultimately requires the performance advantages of cython.

The code utilizes tools from my personal cython library 'geometry.gauss'
and 'algebra.mathx'.  Semantics are loosely: 'C' objects replicate the
semantics of the builtin 'complex' type with additional geometric methods.
'Angle' is essentially a 'float' with unit conversion attributes.

The code also uses, more for my convenience, than critical to calculating
values, my personal 'svg.dom.py' to generate svg fragments.
"""
# standard libraries
from math import sqrt,cos,sin,pi,acos,asin
from operator import mul
# personal libraries
from geometry.gauss import C,Angle
from algebra.mathx import clean,odd
from svg.dom import SVG,Defs,Group,Path,Key,Use,Transform,Rectangle

__all__=['Fillet','Squash_Oring','SqPin','Header','Gauge','heron','pythagoras']
__version__=20180917
__version_history__=(20180827,)

def _tidy(z,n=14):
  """Temporary function - C.tidy uses fixed 15 significant digit rounding.
     cumulative error propagates to the 14th place in some calculations.
     This function implements a variable precision C.tidy."""
  z=map(lambda e: clean(e,n), C(z))
  return C(map(lambda e: e if abs(e)>10**(-n) else 0.0, z))

def heron(a,b,c):
  """Return the area of a triangle with edge lengths 'a','b', and 'c'."""
  t=(a,b,c); s=sum(t)/2.0 # semi-perimeter
  return sqrt(s*reduce(mul,[s-e for e in t]))

def pythagoras(a,b,c):
  """Pass one of 'a','b','c' as 'None'.  Returns that value calculated
     based on the Pythagorean theorem: a^2 + b^2 = c^2."""
  if c is None: return sqrt(a*a+b*b)
  if b is None: return sqrt(c*c-a*a)
  if a is None: return sqrt(c*c-b*b)
  raise ValueError,"One of a,b,c == {},{},{} must be 'None'.".format(a,b,c)


class Fillet(object):
  """Container for calculating a fillet in the corner of a polygon.  The
     arc sector of the fillet defines a symmetrical quadrilateral.

     0) Let 'e' be the edge length adjacent to the corner, 'r' the edge
        length adjacent to the arc sector center, and 'da' the given areal
        residue with the arc sector removed.
     1) Quadrilateral diagonal => two triangles
     2) Equating hypoteneuses and law of cosines =>
           c^2 = 2*r^2*(1-cos(pi-a)) == 2*e^2*(1-cos(a))
        => e^2 = r^2 * (1-cos(pi-a))/(1-cos(a))
     3) Arc tangency to 'e' => two flanking 90 deg corners =>
        area of quadrilateral is r*e =>
           da = sqrt(r^4 * (1-cos(pi-a))/(1-cos(a))) - pi*r^2*(pi-a)/(2*pi)
        =>  r = sqrt( da/(sqrt( (1-cos(pi-a))/(1-cos(a)) )-(pi-a)/2) )"""
  __slots__=('_a','_da')

  def __init__(self,angle,area):
    """Fillet in a polygon corner defined by two edges separated by 'Angle'
       object 'angle', such that the opposite vertex is an arc center, such
       that '180-angle.deg' spans the arc.  Arc tangency implies the remaining
       two angles are 90 degrees, and the opposing edges are orthogonal to
       the implied edges of the given 'angle'.

       'area' is the area of the fillet in the corner."""
    self._a,self._da = Angle(angle),abs(float(area)) # sanitize

  def __repr__(self): return "Fillet({},{})".format(self._a,self._da)

  @property
  def radius(self):
    """Get the radius of the implicit fillet."""
    a,da = self._a.rad,self._da
    return sqrt( da/(sqrt( (1.0-cos(pi-a))/(1.0-cos(a)) )-(pi-a)/2.0) )

  @property
  def edge(self):
    """Get the distance from the corner to the tangent point."""
    a=self._a.rad
    return self.radius*sqrt( (1.0-cos(pi-a)) / (1.0-cos(a)) )


class Squash_Oring(Group):
  """Container for properties of a squashed O-ring"""
  __slots__=('_r','_v','_e','_ta','_ra','_da')

  def __init__(self,radius,triangle):
    """Setup salient geometry for an O-ring with 'radius' cross section
       squashed into a triangular groove abutting a cylinder wall.  The
       'triangle' is passed as a tuple of three 'C' values."""
    super(Squash_Oring,self).__init__()
    self._r,self._v = abs(float(radius)),tuple(map(C,triangle)) # sanitize
    if len(self._v) != 3: raise ValueError, \
      "Triangle {} does not have three vertices.".format(self._v)
    self._e = tuple(abs(self._v[i]-self._v[(i+1)%3]) for i in range(3))
    self._ta=heron(*self._e) # area: Heron's formula
    self._ra=pi*self._r*self._r # O-ring sectional area
    self._da=self._ta-self._ra # differential area
    if self._da <= 0.0: raise ValueError, \
      "Triangle area {} <= {} == O-ring sectional area.".format(self._ta,self._ra)

  def __call__(self,index,proportion):
    """Return a tuple of 'Fillet' properties of the O-ring pressed into
       triangle corner 'index' - an index into the initialization vertices.
       The area of the open 'Fillet' will be a 'proportion' of the difference
       between the area of the triangle and the O-ring section.  The tuple
       returned is:
         (radius,edge,vertex[index],tangent_0,center,tangent_1)"""
    i,p = abs(int(index)%3),min(abs(float(proportion)),1.0) # sanitize
    pts=self._v; v=pts[i]
    a=acos( (pts[(i-1)%3]-v).unit|(pts[(i+1)%3]-v).unit) # arg is inner product
    f=Fillet(Angle(a,'rad'),self._da*p)
    r,e = f.radius,f.edge
    du=(pts[(i-1)%3]-v).unit; dv=du.ortho
    t0=v+e*du; c=t0+r*dv
    t1=v+e*(pts[(i+1)%3]-v).unit
    ret=map(_tidy,[r,e,v,t0,c,t1])
    return tuple( [ret[0].x,ret[1].x]+ret[2:] )

  def __repr__(self): return "Squash_Oring({},{})".format(self._r,self._v)

  def xml(self,svg,proportions):
    """Return an svg xml fragment for this 'Squash_Oring'.  'svg' is a
       the svg.dom.SVG that will contain the O-ring or a dummy used for
       tab management.  'proportions' is a list of the three fillet
       proportions of the residual area."""
    if len(proportions)!=3: raise ValueError, \
      "# of proportions == {} != # corners in a triangle.".format(len(proportions))
    if sum(proportions)!=1.0: raise ValueError, \
      "Residual area proportions sum == {} != 1.0".format(sum(proportions))
    p=Path(); self+=p
    p.fill,p.stroke = "Olive","none"
    p.stroke_width,p.stroke_linejoin = 0.0,"round"
    end=self(2,proportions[2])[-1]
    p.move(end)
    for i in range(3):
      r,s,v,t0,c,t1 = self(i,proportions[i])
      p.line(t0); p.arc(r,t1)
    return super(Squash_Oring,self).xml(svg)


class SqPin(Group):
  """Encapsulate a representation of a header pin and through hole solder
     pad designed for .1" on center spacing.  The representation is
     expressed in millimeters."""
  __slots__=('_r','_cl')

  def __init__(self,radius=.05,clearance=0.03):
    """The 'SqPin' object origin is the pin center.  The pad is a circle of
       radius in inches with two flats so that there is 'clearance'
       inches between adjacent pads on a header.  The pin is a
       .64 mm square (~.025")."""
    super(SqPin,self).__init__(Key("sqpin"))
    self._cl,self._r = map(float,[clearance,radius])
    p,s = Path(Key("pad")),Rectangle(C(0.32,0.32),key=Key("pin"))
    self+=p; self+=s
    p.fill,p.stroke = "Chocolate","none"
    s.fill,s.stroke = "Gold","none"
    r,c = self._r*25.4,self._cl*25.4
    a=Angle(acos((r-c/2.0)/r),'rad'); v=r*C(a)
    p.move(-v); p.arc(r,-~v,False); p.line(v); p.arc(r,~v,False); p.line(-v)

  def __repr__(self): return "Connect({}, {})".format(self._r,self._cl)


class Header(Group):
  """Encapsulate a representation of a multi-pin header with pads designed
     for .1" on center spacing.  The representation is expressed in millimeters."""
  __slots__=('_p','_r','_pin')

  def __init__(self,group,pins=3,reference=1):
    """The 'Header' has 'pins' number of 'svg.dom.group' objects extending
       from the reference pin along the y-axis, .1" on center.  The 'group'
       object represents the appearance of the pin, and must be defined in an
       'svg.dom.Defs' object.  Pins are numbered from zero.  The reference
       pin is located at the origin.  Subsequent pins are along the positive
       y-axis and prior ones are along the negative y-axis."""
    super(Header,self).__init__(Key("header"))
    self._p,self._r = map(int,[pins,reference])
    if not self._r in range(self._p): raise ValueError, \
      "Reference pin {} is not contained in header pins: [0 .. {}]".format( \
         self._r,self.p)
    self._pin=pin=group; uk=Key("pin")
    for i in range(self._p):
      u=Use(pin,uk)
      u.xform=Transform(translate=C(0.0,2.54)*(i-self._r))
      self+=u

  def __repr__(self): return "Header({}, {})".format(self._p,self._r)


class Gauge(Group):
  """Container for calculation of an annular strain gauge conductor pattern."""
  __slots__=('_ir','_or','_w','_r','_cr','_n','_a','_tr','_defs')

  def __init__(self,IR,OR,trace=.25,radius=.75):
    """'IR' is the inside radius of the available annulus for gauge wires
       and 'OR' is the outside radius.  The gauge pattern will provide a
       minimum clearance for 'trace' width gauge wires of distance 'radius'
       within that annulus.  The value 'radius' is also the radius of turns
       in the pattern."""
    super(Gauge,self).__init__(Key("assembly"))
    self._ir,self._or,self._w,self._r = map(float,[IR,OR,trace,radius]) # sanitize
    self._cr=self._ir+2.0*self._r+self._w  # minimum center radius
    self._n=int(pi/asin(self._r/self._cr)) # number of radial traces that fit
    self._n += 1 if odd(self._n) else 2    # normalize
    self._a=Angle(1.0/self._n)             # half angle between traces
    self._cr=self._r/sin(self._a.rad)      # adjusted center radius
    self._tr=self._or-self._r-.5*self._w   # outside trace radius
    self._defs=d=Defs()
    self+=d; d+=self.hairpin; d+=self.splice; d+=self.section
    sqp=SqPin(); d+=sqp; hdr=Header(sqp); hdr.xform=Transform(rotate=-4.0*self._a)
    d+=hdr; d+=self.gauge; d+=self.inside_sensor; d+=self.outside_sensor

  def __repr__(self): return "Gauge({},{},{},{})".format( \
                              self._ir,self._or,self._w,self._r)

  @property
  def center_radius(self):
    """Get radius of the centers of the inside hairpin turns in the traces
       of the gauge pattern."""
    return self._cr

  @property
  def trace_radius(self):
    """Get radius of the peripheral trace center that splices hairpins
       of the gauge pattern."""
    return self._tr

  @property
  def legs(self):
    """Get the number of radial traces in the gauge pattern."""
    return self._n

  @property
  def angle(self):
    """Get the angle between radial traces in the gauge pattern in degrees."""
    return self._a.deg*2.0

  @property
  def hairpin(self):
    """Get an svg.dom.Group representing the inner turn and two legs."""
    g,p = Group(Key("hairpin")),Path(Key("arc")); g+=p
    g.xform=Transform(translate=C(0.0,-self._cr))
    p.fill,p.stroke = "none","Chocolate"
    p.stroke_width,p.stroke_linejoin = self._w,"round"
    r,a,d = self._r,self._a,C(0.0,self._cr)
    t,e = r*C(a),C(0.0,pythagoras(None,r,self._tr-r))*C(a)-d # tangent,end
    p.move(~e); p.line(-~t); p.arc(r,t,False); p.line(-e)
    return g

  @property
  def splice(self):
    """Get an svg.dom.Group representing two outer traces and a connecting hairpin."""
    g,p = Group(Key("splice")),Path(Key("base")); g+=p
    g.xform=Transform(translate=C(0.0,-self._cr))
    p.fill,p.stroke = "none","Chocolate"
    p.stroke_width,p.stroke_linejoin = self._w,"round"
    r,a,tr,d = self._r,self._a,self._tr,C(0.0,self._cr)
    e = C(0.0,pythagoras(None,r,self._tr-r))*C(a) - d # end
    t = ( C(0.0,tr) + ~C(a)*r )*C(a) - d # tangent
    p.move(~e); p.arc(r,~t); p.arc(tr,-t); p.arc(r,-e)
    return g

  @property
  def section(self):
    """Get an svg.dom.Group representing a hairpin and two splices."""
    g=Group(Key("section")); uk=Key("trace")
    sr = [d for d in self._defs if d.key.count("splice")>0][0]
    hr = [d for d in self._defs if d.key.count("hairpin")>0][0]
    a=Angle(self.angle,'deg')
    u=Use(sr,uk); u.xform=Transform(rotate=-a); g+=u
    u=Use(hr,uk); g+=u
    u=Use(sr,uk); u.xform=Transform(rotate= a); g+=u
    return g

  @property
  def gauge(self):
    """Get a sequence of SVG use statements representing the gauge."""
    g=Group(Key("gauge")); uk=Key("part")
    spr = [d for d in self._defs if d.key.count("splice")>0][0]
    sr = [d for d in self._defs if d.key.count("section")>0][0]
    hr = [d for d in self._defs if d.key.count("hairpin")>0][0]
    a=Angle(2.0*self.angle,'deg'); m=self._n>>1
    if odd(m):
      cp=m+1>>1; cm=cp-1
      u=Use(hr,uk); u.xform=Transform(rotate=-a*cm); g+=u
      u=Use(spr,uk); u.xform=Transform(rotate=-a*cm+a/2.0); g+=u
    else:
      cp=cm=m>>1; u=Use(hr,uk); u.xform=Transform(rotate=-a*cm); g+=u
    for i in range(-cm+1,0):
      if odd(i):
        u=Use(sr,uk); u.xform=Transform(rotate=a*i); g+=u
      else:
        u=Use(hr,uk); u.xform=Transform(rotate=a*i); g+=u
    for i in range(1,cp):
      if odd(i):
        u=Use(sr,uk); u.xform=Transform(rotate=a*i); g+=u
      else:
        u=Use(hr,uk); u.xform=Transform(rotate=a*i); g+=u
    hr = [d for d in self._defs if d.key.count("header")>0][0]
    z=C(0.0,-(self._ir+self._or)/2.0)*C(-self._a/1.618)
    u=Use(hr,uk); u.xform=Transform(translate=z); g+=u
    return g

  @property
  def inside_sensor(self):
    """Get a 'gauge' customized for the inside."""
    g,p = Group(Key("inside_sensor")),Path(Key("patch_i")); g+=p
    sr = [d for d in self._defs if d.key.count("gauge")>0][0]
    u=Use(sr,Key("sensor_i")); g+=u
    p.fill,p.stroke = "none","Chocolate"
    p.stroke_width,p.stroke_linejoin = self._w,"round"
    p.xform=Transform(translate=C(0.0,-self._cr))
    r,a,d = self._r,self._a,C(0.0,self._cr)
    s=C(0.0,pythagoras(None,r,self._tr-r))*C(a)-d # start
    e=-r*C(a)-s; e0,e1 = s+e*.1,s+e*.9
    p.move(~s); p.line(~e0); p.move(-s); p.line(-e1)
    return g

  @property
  def outside_sensor(self):
    """Get a 'gauge' customized for the ouside."""
    g,p = Group(Key("outside_sensor")),Path(Key("patch_o")); g+=p
    sr = [d for d in self._defs if d.key.count("gauge")>0][0]
    u=Use(sr,Key("sensor_o")); g+=u
    p.fill,p.stroke = "none","Chocolate"
    p.stroke_width,p.stroke_linejoin = self._w,"round"
    p.xform=Transform(translate=C(0.0,-self._cr))
    r,a,d = self._r,self._a,C(0.0,self._cr)
    s=C(0.0,pythagoras(None,r,self._tr-r))*C(a)-d # start
    e=-r*C(a)-s; e0,e1 = s+e*.1,s+e*.4; e2=e1+r*C(a)-r*C(a)*1j
    p.move(~s); p.line(~e0); p.move(-s); p.line(-e1); p.arc(r,-e2)
    return g


if __name__=="__main__":
  # 2 mm diagonal half square groove; 1 mm diameter O-ring
  s=SVG() # dummy svg header providing indentation reference.
  sor=Squash_Oring(0.5, [C(0.0,1.0),C(1.0,0.0),C(0.0,-1.0)])
  print sor,repr(sor)
  thrd=1./3.
  data=[sor(i,p) for i,p in zip(range(3),(thrd,thrd,thrd))]
  for i in range(3):
    print i,data[i][:3]
    for z in data[i][3:]: print "  ",repr(z)
  print
  print sor.xml(s,(thrd,thrd,thrd))
  # Calculations for strain gauge
  g=Gauge(7.5,18.0)
  print g,repr(g),g.center_radius,g.trace_radius,g.legs,g.angle
  print
  print g.xml(s)
