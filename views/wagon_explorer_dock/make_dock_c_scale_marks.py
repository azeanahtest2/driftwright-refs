"""Scale marks on dock take C (Aaron, 27 Nov 10:08: "C is closest - now rebuild the concept to scale: doors & steps, bay door, bridge should be updated to the correct scale").
True sizes from Joe's wagon_interior.gd (unscaled: hatch 1.3 x 2.3 m, sill 1.95 m) and the dwarf (1.5 m, player.gd v027). Take C is 59 px/m, ground at y 928."""
import numpy as np
from PIL import Image, ImageDraw
im=Image.open('/tmp/wd/take3.png').convert('RGBA'); g=ImageDraw.Draw(im)
PPM=59.0; GND=928; Y=lambda h:round(GND-h*PPM); X=lambda x,m:round(x+m*PPM)
C=(0,220,255,255); W=5
def r(x0,x1,h0,h1): g.rectangle([x0,Y(h1),x1,Y(h0)],outline=C,width=W)
# side hatch 1.3 x 2.3, sill 1.95, at the present hatch
SILL=2.0*1.18                                       # her living deck, scaled with the hull (2.36 m)
hx=457; r(X(hx,-0.65),X(hx,0.65),SILL,SILL+2.3)
# folding steps from the sill to the ground: six steps of 0.325 m, 0.7 m wide
for k in range(7):
    h=SILL-k*SILL/7; g.line([X(hx,-0.35),Y(h),X(hx,0.35),Y(h)],fill=C,width=W)
g.line([X(hx,-0.35),Y(SILL),X(hx,-0.35),Y(0)],fill=C,width=3); g.line([X(hx,0.35),Y(SILL),X(hx,0.35),Y(0)],fill=C,width=3)
# the roof ladder: rungs 0.3 m apart, 0.5 m wide
lx=590
for h in np.arange(0.4,6.9,0.3): g.line([X(lx,-0.25),Y(h),X(lx,0.25),Y(h)],fill=C,width=3)
# bay door (the hazard panel midships): a crew and cargo door, 2.0 x 2.3 m, sill on the deck at 1.95 m
bx=821; r(X(bx,-1.0),X(bx,1.0),SILL,SILL+2.3)
# bridge: four panes 0.5 x 0.6 m at a dwarf's eye on a bridge deck at 4.4 m (eye 5.65 m)
# bridge: the helm on Joe's cockpit deck (2.36 m), eye at 3.6 m: a band of panes 0.5 x 0.7 m, 3.2-3.9 m, round the cab's nose
for k in range(4): x0=X(95,k*0.6); r(x0,x0+round(0.5*PPM),SILL+0.85,SILL+1.55)
g.line([X(85,0),Y(SILL),X(330,0),Y(SILL)],fill=C,width=3)
# dwarves, 1.5 m: on the ground by the steps, and in the hatch
def cut(p):
    a=np.asarray(Image.open(p).convert('RGB')).astype(int); bg=a[3,3]; m=np.abs(a-bg).sum(2)>40; ys,xs=np.where(m)
    d=Image.open(p).convert('RGBA').crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); d.putalpha(Image.fromarray((m[ys.min():ys.max()+1,xs.min():xs.max()+1]*255).astype(np.uint8))); return d
d=cut('/home/claude/driftwright-refs/views/grimrivet_restyle/front.png'); s=1.5*PPM/d.height; d=d.resize((round(d.width*s),round(d.height*s)),Image.LANCZOS)
im.alpha_composite(d,(X(hx,0.9),GND-d.height)); im.alpha_composite(d,(hx-d.width//2,Y(SILL)-d.height)); im.alpha_composite(d,(X(150,0),Y(SILL)-d.height))
im.convert('RGB').save('/tmp/wd/wagon_dock_c_scale_marks.png')
