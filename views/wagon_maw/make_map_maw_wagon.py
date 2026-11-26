"""True-scale map: the 1.18x Wagon (23.0 m) with Brokkr's Wake's bridge and maw reduced onto her nose (Aaron, 26 Nov 14:55).
Lower deck: the maw, the ore catcher and the debris conveyor running aft to the rear bay. Upper deck: the bridge at the brow, then
the living quarters (Joe's rooms in his order), then an airlock into the bay. The Explorer docks aft as the tail gun (map B, trimmed)."""
from PIL import Image, ImageDraw, ImageFont
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26); F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18); FS=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
K=1.18; XI=2.15*K; XO=XI+0.2                        # inside / outside half-width
L=23.0; ROOF=6.6*K; LOW=1.0; UP=4.0; CEIL=6.8; DOCK=3.0*K
EX_L,EX_W,EX_H=7.4,4.4,3.8
R={'bridge':(0.6,4.6),'equip':(4.6,8.6),'galhead':(8.6,11.7),'bunks':(11.7,14.0),'lock':(14.0,15.6)}
EZ0=R['lock'][1]+2.0; EZ1=EZ0+EX_L                   # her bow 2 m past the 23 m stern
PPM=50; M=60
W=round((EZ1+2)*PPM)+2*M+520; out=Image.new('RGB',(W,1900),(240,238,232)); g=ImageDraw.Draw(out)
g.text((M,20),"The Wagon with Brokkr's bridge and maw: true-scale map (23.0 m, the Explorer docked aft as her tail gun)",fill=(20,20,20),font=FB)
_rect=ImageDraw.ImageDraw.rectangle; _ell=ImageDraw.ImageDraw.ellipse
def _fix(xy):
    (a,b),(c,d)=xy; return [(min(a,c),min(b,d)),(max(a,c),max(b,d))]
ImageDraw.ImageDraw.rectangle=lambda self,xy,*a,**k:_rect(self,_fix(xy),*a,**k)
ImageDraw.ImageDraw.ellipse=lambda self,xy,*a,**k:_ell(self,_fix(xy),*a,**k)
def plan(y0,title):
    P=lambda z,x:(M+z*PPM,y0+(x+XO)*PPM)
    g.text((M,y0-34),title,fill=(30,30,30),font=F)
    g.rectangle([P(0,-XO),P(L,XO)],fill=(205,205,212),outline=(60,60,60),width=2); return P
def box(P,z0,z1,x0,x1,c,t=None,tx=None):
    g.rectangle([P(z0,x0),P(z1,x1)],fill=c,outline=(70,70,70),width=2)
    if t: g.text(P(z0+0.15,(tx if tx is not None else x0+0.15)),t,fill=(30,30,30),font=FS)
# ---- upper deck
P=plan(120,'Upper deck, floor 4.0 m: bridge at the brow, living quarters, airlock to the bay (port at the top, nose to the left)')
g.polygon([P(0,-XO),P(0.6,-XI),P(0.6,XI),P(0,XO)],fill=(255,170,60))
g.text(P(0.05,XO+0.15),'brow windows',fill=(150,70,10),font=FS)
box(P,*R['bridge'],-XI,XI,(233,214,170),'bridge\nhelm, sensors,\nclaw controls')
box(P,*R['equip'],-XI,XI,(214,226,214),'equipment (Joe\'s)')
for sx in (-1,1): g.rectangle([P(5.5,sx*XO-0.15),P(7.0,sx*XO+0.15)],fill=(210,170,40))
g.text(P(4.75,0.4),'side hatches;\nladders down',fill=(60,60,60),font=FS)
box(P,R['galhead'][0],R['galhead'][1],-XI,-0.2,(236,216,196),'galley'); box(P,R['galhead'][0],R['galhead'][1],0.6,XI,(206,222,236),'head')
box(P,R['bunks'][0],R['bunks'][1],-XI,XI,(226,206,226),'bunks')
box(P,*R['lock'],-1.2,1.2,(250,200,120),'airlock'); 
for z in R['lock']: g.line([P(z,-XI),P(z,XI)],fill=(40,40,40),width=5)
g.rectangle([P(R['lock'][1],-XI),L and P(L,XI)],fill=(196,200,208),outline=(70,70,70),width=2)
g.text(P(R['lock'][1]+0.15,XO+0.15),'rear bay: dock deck 3.5 m, a short step down from the airlock',fill=(30,30,30),font=FS)
g.rectangle([P(R['lock'][1],-0.85),P(EZ0,0.85)],fill=(210,170,60),outline=(120,60,20),width=2)
g.text(P(R['lock'][1]+0.15,0.95),'her stern ramp lands here',fill=(120,50,10),font=FS)
ex=Image.open('/tmp/rmp/explorer_ramp.png').convert('RGB'); Wd,Hd=ex.size
import numpy as np
def cut(im):
    a=np.asarray(im).astype(int); bg=a[3,3]; m=np.abs(a-bg).sum(2)>36; ys,xs=np.where(m)
    im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).convert('RGBA'); im.putalpha(Image.fromarray((m[ys.min():ys.max()+1,xs.min():xs.max()+1]*255).astype(np.uint8))); return im
from PIL import ImageOps
top=ImageOps.mirror(cut(ex.crop((0,int(Hd*0.5),int(Wd*0.45),Hd)))).resize((round(EX_L*PPM),round(EX_W*PPM)))
out.paste(top,(round(P(EZ0,0)[0]),round(P(0,-EX_W/2)[1])),top)
g.line([P(L,-XO),P(L,XO)],fill=(200,120,40),width=7); g.text(P(L+0.1,-XO-0.6),'gasket collar',fill=(120,50,10),font=FS)
# ---- lower deck
P=plan(560,'Lower deck, floor 1.0 m: the maw, ore catcher, the conveyor to the rear bay, and the service stations to port')
g.polygon([P(0,-1.8),P(0,1.8),P(1.2,1.6),P(1.2,-1.6)],fill=(60,40,30)); g.text(P(0.05,XO+0.15),'the maw (open to space)',fill=(30,30,30),font=FS)
box(P,1.2,4.6,-XI,XI,(150,120,95))
for k in range(7): z=1.4+k*0.45; g.line([P(z,-1.7),P(z+0.3,0),P(z,1.7)],fill=(90,70,50),width=3)
g.text(P(1.3,-XI+0.1),'ore catcher:\ngrate and\ncrusher jaws',fill=(250,240,220),font=FS)
# conveyor along the starboard wall, walkway down the middle, the service stations to port (Aaron, 15:04)
box(P,4.6,R['lock'][1]+2.0,0.9,XI,(110,110,118))
for z in np.arange(4.8,R['lock'][1]+2.0,0.5): g.line([P(z,0.9),P(z,XI)],fill=(70,70,78),width=2)
g.text(P(5.0,1.3),'debris conveyor, 1.6 m belt, running aft  >>>',fill=(240,240,240),font=FS)
box(P,4.6,R['lock'][1],-0.25,0.9,(222,222,226)); g.text(P(9.4,0.05),'walkway',fill=(60,60,60),font=FS)
ST=[(4.8,5.8,-XI,-1.3,(196,160,120),'claw\npost'),(6.0,7.0,-XI,-1.3,(196,180,150),'hold\ncontrol\npost'),
    (7.3,11.8,-XI+0.05,-0.35,(150,110,90),'long boiler: the Hammerhead\'s\nforge-pit boiler, 4.5 m,\nlying lengthwise'),
    (12.1,13.5,-XI,-0.9,(176,170,190),'fabricator'),(13.7,15.4,-XI,-1.2,(190,190,170),'parts and\ntool racks')]
for z0,z1,x0,x1,c,t in ST: box(P,z0,z1,x0,x1,c,t)
box(P,R['lock'][1],R['lock'][1]+2.6,-XI,XI,(170,140,100),'ore hopper\n(under the\ndock deck)')
box(P,R['lock'][1]+2.6,L,-XI,XI,(190,170,150),'engines; the hopper\nchutes to the\ncargo bins')
# ---- section from port
y0=1440; S=lambda z,h:(M+z*PPM,y0-h*PPM)
g.text((M,y0-ROOF*PPM-70),'Section from port',fill=(30,30,30),font=F)
g.line([S(-1,0),S(EZ1+1,0)],fill=(120,120,120),width=2)
g.rectangle([S(0.6,ROOF),S(L,0.6)],fill=(205,205,212),outline=(60,60,60),width=2)
g.polygon([S(0,0.9),S(0.6,0.6),S(0.6,ROOF),S(0,ROOF-0.9)],fill=(205,205,212),outline=(60,60,60))
g.rectangle([S(0,LOW),S(1.2,3.6)],fill=(60,40,30))                     # maw mouth
g.polygon([S(-0.5,3.4),S(1.6,3.9),S(1.6,4.3),S(-0.2,4.1)],fill=(190,165,120),outline=(90,70,40))   # moustache plates
g.text(S(1.4,3.85),'moustache plates over the maw',fill=(80,60,30),font=FS)
g.rectangle([S(0,5.0),S(0.6,6.1)],fill=(255,170,60)); g.text(S(0.8,7.5),'brow windows (the bridge)',fill=(150,70,10),font=FS)
g.line([S(0.6,UP),S(R['lock'][1],UP)],fill=(50,50,50),width=4); g.line([S(0.6,CEIL),S(R['lock'][1],CEIL)],fill=(130,130,130),width=2)
g.line([S(0.6,LOW),S(R['lock'][1]+2.6,LOW)],fill=(50,50,50),width=4)
for k,(n,(a,b)) in enumerate(R.items()):
    g.line([S(b,UP),S(b,CEIL)],fill=(90,90,90),width=2)
    g.text(S(a+0.15,UP+2.3-(k%2)*0.5),{'bridge':'bridge','equip':'equipment','galhead':'galley / head','bunks':'bunks','lock':'airlock'}[n],fill=(30,30,30),font=FS)
g.text(S(1.3,2.9),'ore catcher',fill=(30,30,30),font=FS)
g.rectangle([S(4.6,1.25),S(R['lock'][1]+1.2,1.55)],fill=(110,110,118)); g.text(S(4.7,3.5),'conveyor (starboard), runs aft >>>',fill=(30,30,30),font=FS)
g.rounded_rectangle([S(7.3,3.1),S(11.8,1.0)],radius=22,fill=(150,110,90),outline=(80,50,40),width=2); g.text(S(7.5,2.4),'long boiler (port side)',fill=(250,235,220),font=FS)
g.rectangle([S(12.1,2.6),S(13.5,1.0)],fill=(176,170,190),outline=(70,70,70),width=2); g.text(S(12.15,2.3),'fabricator',fill=(30,30,30),font=FS)
g.polygon([S(R['lock'][1],DOCK-0.2),S(R['lock'][1]+2.6,DOCK-0.2),S(R['lock'][1]+1.8,1.0),S(R['lock'][1]+0.8,1.0)],fill=(170,140,100),outline=(90,70,40))
g.text(S(R['lock'][1]+2.7,2.0),'ore hopper',fill=(30,30,30),font=FS)
g.line([S(R['lock'][1],DOCK),S(L,DOCK)],fill=(50,50,50),width=4); g.text(S(R['lock'][1]+0.2,DOCK+0.3),'dock deck 3.5 m',fill=(30,30,30),font=FS)
g.ellipse([S(L-2.4,2.6),S(L-0.4,0.6)],fill=(230,140,50)); g.text(S(R['lock'][1]+3.0,0.9),'engines',fill=(30,30,30),font=FS)
es=cut(ex.crop((int(Wd*0.62),0,Wd,int(Hd*0.5)))); es=es.resize((round(EX_L*PPM),round(es.height*EX_L*PPM/es.width)))
es=es.crop((0,max(0,es.height-round(EX_H*PPM)),es.width,es.height)); out.paste(es,(round(S(EZ0,0)[0]),round(S(0,DOCK)[1])-es.height),es)
g.line([S(L,DOCK),S(L,DOCK+4.2)],fill=(200,120,40),width=7)
for k in range(5):                                                       # the claws, folded under the chin when landed
    z=0.1+k*0.25; g.line([S(z,LOW-0.1),S(z+0.5,0.35),S(z+0.1,0.15)],fill=(170,120,50),width=6)
g.text(S(-1.0,-0.7),'five beard claws, folded under the chin when landed',fill=(120,70,20),font=FS)
g.line([S(0,-1.4),S(L,-1.4)],fill=(60,60,60),width=1); g.text(S(9,-1.35),'hull 23.0 m, the Explorer 2 m beyond',fill=(30,30,30),font=FS)
for h,t in [(LOW,'1.0'),(UP,'4.0'),(CEIL,'6.8'),(ROOF,'7.8 roof')]: g.text(S(-1.15,h+0.25),t,fill=(90,90,90),font=FS)
# ---- front view
fx=round(S(EZ1+1.2,0)[0])+60; FY=y0; Fv=lambda x,h:(fx+(x+XO)*PPM,FY-h*PPM)
g.text((fx,FY-ROOF*PPM-70),'Front',fill=(30,30,30),font=F)
g.rectangle([Fv(-XO,ROOF),Fv(XO,0.6)],fill=(200,195,185),outline=(60,60,60),width=2)
g.rectangle([Fv(-XO+0.3,5.0),Fv(XO-0.3,6.1)],fill=(255,170,60))
g.text(Fv(-XO+0.4,6.6),'bridge: brow windows',fill=(30,30,30),font=FS)
g.rectangle([Fv(-1.8,LOW),Fv(1.8,3.6)],fill=(60,40,30)); g.text(Fv(-1.6,2.5),'maw 3.6 x 2.6 m',fill=(240,200,150),font=FS)
for sx in (-1,1): g.polygon([Fv(0,4.4),Fv(sx*XO,3.4),Fv(sx*XO,3.0),Fv(sx*0.3,3.6)],fill=(190,165,120),outline=(90,70,40))
for k in range(5):
    x=-2.0+k*1.0; g.line([Fv(x,LOW),Fv(x,0.5)],fill=(170,120,50),width=8); g.ellipse([Fv(x-0.3,0.55),Fv(x+0.3,0.05)],outline=(170,120,50),width=5)
g.text(Fv(-XO,-0.6),'width 5.5 m',fill=(30,30,30),font=FS)
out=out.crop((0,0,fx+round(2*XO*PPM)+200,1560)); out.save('/tmp/mw/maw_wagon_map.png'); print(out.size)
