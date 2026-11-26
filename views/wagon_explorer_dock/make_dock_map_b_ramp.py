"""True-scale maps of the scaled-up Wagon with the Mine Cart Explorer docked facing aft as her tail gun.
Rooms from Joe's wagon_interior.gd (Driftwright modules/wagon) scaled 1.18x; the dock and Explorer per Aaron 26 Nov 13:57 and 14:12.
Frame as Joe's: z along her (nose at -z, drawn left), x across (port negative, drawn at the top)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
K=1.18
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24); F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17); FS=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
# Joe's frame (metres), scaled
NOSE_SKIN=-9.6*K; Z_NOSE=-8.3*K; Z_CK=-4.7*K; HATCH_Z=-3.52*K; HATCH_W=1.3*K; GAL=(-1.5*K,1.1*K); BUNK=(1.3*K,3.25*K); Z_AFT=3.3*K
X_IN=2.15*K; DECK=2.0*K; CEIL=4.6*K
EX_L,EX_W,EX_H=7.4,4.4,3.8; SIDE=1.5; DOCK_X=EX_W/2+SIDE; HULL_X=DOCK_X+0.5     # 3.7 inside, 4.2 outside
DOCK_Z0=Z_AFT+0.35
exs=Image.open('/tmp/mc/explorer_views.png').convert('RGB'); W,H=exs.size
def cut(im):
    a=np.asarray(im).astype(int); bg=a[3,3]; m=np.abs(a-bg).sum(2)>36; ys,xs=np.where(m)
    im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); m=m[ys.min():ys.max()+1,xs.min():xs.max()+1]
    r=im.convert('RGBA'); r.putalpha(Image.fromarray((m*255).astype(np.uint8))); return r
ex_top=ImageOps.mirror(cut(exs.crop((0,int(H*0.5),int(W*0.45),H))))      # bow right (aft), her port at the bottom = Wagon starboard
ex_stbd=cut(exs.crop((int(W*0.62),0,W,int(H*0.5))))                     # her starboard side, bow right: what you see from the Wagon's port side
OPTIONS=[('A','Flush: her nose at the Wagon\'s tail, guns through two armoured ports',0.0,'dock 2 m clear ahead of her'),
 ('B','Tail turret: her nose and guns 2 m out of the stern, a gasket collar seals round her hull',2.0,'the Wagon 2 m shorter for the same dock'),
 ('C','Slide-out: she rides a rail cradle 1 m out to fire, back in to seal (drawn run out)',1.0,'')]
PPM=42
def plan_and_section(tag,title,out_m,note):
    # the Wagon's stern: dock 2 m ahead of her + her length, less what sticks out
    ez0=DOCK_Z0+2.0; ez1=ez0+EX_L; stern=ez1-out_m+(0.0 if out_m else 0.0)
    if tag=='A': stern=ez1
    if tag=='B': stern=ez1-2.0
    if tag=='C': stern=ez1-1.0
    L=stern-NOSE_SKIN
    mx0=NOSE_SKIN-1.0; mx1=max(stern,ez1)+1.5
    pw=round((mx1-mx0)*PPM)+40; ph=round(2*HULL_X*PPM)+110; sh=round(9.5*PPM)+70
    img=Image.new('RGB',(pw*2+60,ph+120),(240,239,236)); g=ImageDraw.Draw(img)
    g.text((20,8),f'{tag}. {title}',fill=(30,30,30),font=FB)
    # ---- plan
    ox=20; oy=95
    def P(z,x): return (ox+(z-mx0)*PPM, oy+(x+HULL_X)*PPM)
    def rect(z0,z1,x0,x1,fill,outline=(70,70,70),w=2): g.rectangle([P(z0,x0),P(z1,x1)],fill=fill,outline=outline,width=w)
    rect(NOSE_SKIN,Z_AFT+0.35,-X_IN-0.2,X_IN+0.2,(205,205,212))           # body
    rect(DOCK_Z0,stern,-X_IN-0.2,X_IN+0.2,(196,200,208))                     # dock section
    rect(NOSE_SKIN+0.4,Z_CK,-1.95*K,1.95*K,(230,214,170)); g.text(P(Z_NOSE+0.3,-0.4),'cockpit',fill=(40,40,40),font=FS)
    rect(Z_CK,GAL[0],-X_IN,X_IN,(214,226,214)); g.text(P(Z_CK+0.2,-0.4),'equipment',fill=(40,40,40),font=FS)
    for sx in (-1,1): g.rectangle([P(HATCH_Z-HATCH_W/2,sx*(X_IN+0.2)-0.15),P(HATCH_Z+HATCH_W/2,sx*(X_IN+0.2)+0.15)],fill=(210,170,40))
    rect(GAL[0],GAL[1],-X_IN,-0.2,(236,216,196)); g.text(P(GAL[0]+0.2,-X_IN+0.4),'galley',fill=(40,40,40),font=FS)
    rect(GAL[0],GAL[1],0.6*K,X_IN,(206,222,236)); g.text(P(GAL[0]+0.2,0.9*K),'head',fill=(40,40,40),font=FS)
    rect(BUNK[0],BUNK[1],X_IN-1.15,X_IN,(226,206,226)); g.text(P(BUNK[0]+0.1,X_IN-1.0),'bunks',fill=(40,40,40),font=FS)
    g.line([P(Z_AFT,-X_IN),P(Z_AFT,X_IN)],fill=(60,60,60),width=4)
    # the dock: clamps, walkway to starboard, the pressure collar on the starboard wall
    rect(ez0-0.2,ez1+0.2,-EX_W/2-0.2,EX_W/2+0.2,None,(200,150,40),2)
    k=PPM*EX_L/ex_top.width; t=ex_top.resize((round(ex_top.width*k),round(EX_W*PPM)),Image.LANCZOS)
    img.paste(t,(round(P(ez0,0)[0]),round(P(0,-EX_W/2)[1])),t)
    # her stern ramp (1.2 m wide) folds forward onto the dock deck; a pressure collar on the dock's forward wall seals round it
    g.rectangle([P(ez0-1.4,-0.85),P(ez0,0.85)],fill=(210,170,60),outline=(120,60,20),width=2)
    for k in range(4): zz=ez0-1.4+0.3+k*0.3; g.line([P(zz,-0.7),P(zz,0.7)],fill=(120,90,30),width=2)
    g.rectangle([P(DOCK_Z0,-1.0),P(DOCK_Z0+0.35,1.0)],fill=(200,120,40),outline=(120,60,20),width=2)
    g.text(P(DOCK_Z0+0.1,-X_IN-0.75),'her stern ramp down; pressure collar',fill=(120,50,10),font=FS)
    g.rectangle([P(Z_AFT,-1.0),P(Z_AFT+0.35,1.0)],fill=(200,120,40))   # the door aft of the bunks, on the centre line
    g.text(P(DOCK_Z0+0.1,X_IN+0.35),'centre-line door; about 0.35 m clear each side of her',fill=(40,40,40),font=FS)
    g.text(P(DOCK_Z0+0.1,-X_IN-1.35),'dock deck (over the engines), trimmed to the hull width',fill=(40,40,40),font=FS)
    if tag=='B': g.text(P(stern+0.1,-X_IN-0.75),'gasket collar',fill=(120,50,10),font=FS); g.line([P(stern,-X_IN-0.2),P(stern,X_IN+0.2)],fill=(200,120,40),width=6)
    if tag=='A':
        for sx in (-1,1): g.rectangle([P(stern-0.2,sx*1.3-0.35),P(stern+0.05,sx*1.3+0.35)],fill=(200,120,40))
        g.text(P(stern-3.2,-EX_W/2-0.9),'gun ports',fill=(120,50,10),font=FS)
    if tag=='C': g.line([P(ez0-0.5,-1.2),P(stern+1.0,-1.2)],fill=(90,90,90),width=3); g.line([P(ez0-0.5,1.2),P(stern+1.0,1.2)],fill=(90,90,90),width=3); g.text(P(stern+0.1,-EX_W/2-0.9),'rail cradle',fill=(90,90,90),font=FS)
    # dims
    def dim(z0,z1,x,txt):
        a=P(z0,x); b=P(z1,x); g.line([a,b],fill=(30,30,30),width=1); g.line([(a[0],a[1]-6),(a[0],a[1]+6)],fill=(30,30,30)); g.line([(b[0],b[1]-6),(b[0],b[1]+6)],fill=(30,30,30))
        tw=g.textlength(txt,font=FS); g.text(((a[0]+b[0])/2-tw/2,a[1]+3),txt,fill=(30,30,30),font=FS)
    dim(NOSE_SKIN,stern,HULL_X+0.6,f'hull {L:.1f} m'+(f', the Explorer {max(0,ez1-stern):.0f} m beyond' if ez1>stern else ''))
    dim(DOCK_Z0,ez0,HULL_X+1.5,'2 m'); dim(ez0,ez1,HULL_X+1.5,'Explorer 7.4 m, facing aft')
    g.text((ox,oy-50),'Plan (port at the top, her nose to the left)',fill=(70,70,70),font=F)
    # ---- section (seen from port)
    sx0=pw+40; sy=oy+sh-40
    def S(z,y): return (sx0+(z-mx0)*PPM, sy-y*PPM)
    g.text((sx0,oy-50),'Section from port (her dish folded when docked)',fill=(70,70,70),font=F)
    g.line([S(mx0,0),S(mx1,0)],fill=(140,140,140),width=2)
    g.rectangle([S(NOSE_SKIN,6.6*K),S(Z_AFT+0.35,1.0)],outline=(70,70,70),width=2,fill=(205,205,212))
    g.rectangle([S(DOCK_Z0,6.6*K),S(stern,1.0)],outline=(70,70,70),width=2,fill=(196,200,208))
    g.line([S(NOSE_SKIN+0.4,DECK),S(Z_AFT,DECK)],fill=(60,60,60),width=3); g.line([S(NOSE_SKIN+0.4,CEIL),S(Z_AFT,CEIL)],fill=(120,120,120),width=1)
    bay_deck=3.0*K; g.line([S(DOCK_Z0,bay_deck),S(stern,bay_deck)],fill=(60,60,60),width=3)
    g.text(S(Z_CK+0.2,DECK+1.2),'living deck 2.4 m, 3.1 m clear',fill=(40,40,40),font=FS)
    k=PPM*EX_L/ex_stbd.width; s=ex_stbd.resize((round(ex_stbd.width*k),round(ex_stbd.height*k)),Image.LANCZOS)
    hmax=round(EX_H*PPM)
    if s.height>hmax: s=s.crop((0,s.height-hmax,s.width,s.height))
    img.paste(s,(round(S(ez0,0)[0]),round(S(0,bay_deck)[1])-s.height),s)
    for e in range(1): g.ellipse([S(stern-1.6,2.6),S(stern-0.2,1.2)],fill=(230,140,40),outline=(120,60,20))
    g.text(S(DOCK_Z0+0.1,bay_deck-0.6),'dock deck 3.5 m (engines below)',fill=(40,40,40),font=FS)
    roof=6.6*K; g.text(S(DOCK_Z0+0.1,roof+0.5),f'{roof-bay_deck:.1f} m clear over the dock deck; she is 3.8 m with her dish folded',fill=(40,40,40),font=FS)
    if note: g.text((sx0,sy+18),note,fill=(90,90,90),font=FS)
    return img
rows=[plan_and_section(*OPTIONS[1])]
Wt=max(r.width for r in rows); Ht=sum(r.height for r in rows)+70
out=Image.new('RGB',(Wt,Ht),(240,239,236)); g=ImageDraw.Draw(out)
g.text((20,15),'Option B with the stern ramp: the Explorer faces aft as the tail gun; her stern ramp opens forward into the Wagon (true scale)',fill=(20,20,20),font=FB)
y=60
for r in rows: out.paste(r,(0,y)); y+=r.height
out.save('/tmp/sc/wagon_dock_map_b_ramp.png'); print(out.size)
