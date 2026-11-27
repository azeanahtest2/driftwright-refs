"""Fleet scale lineup, four lanes (Aaron, 27 Nov 12:34). True sizes from docs/class-specs.md and the builds:
dwarf 1.5 m (player.gd v027); Mine Cart round 4 and the new variant 7.2 m; Mine Cart v3 7.2 m; the Explorer 7.4 m;
Splitter 12.7 m; Pounder 18 m (D-B6); Wagon 19 m; Hammerhead 45 m; Anvilhawk 125 m; Anvilguard 155 m overall; Brokkr's Wake 300 m."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R='/home/claude/driftwright-refs/views'
def cut(img, box=None):
    im=Image.open(img).convert('RGB') if isinstance(img,str) else img
    if box: im=im.crop(box)
    a=np.asarray(im).astype(int); bg=a[3,3]; m=np.abs(a-bg).sum(2)>36
    ys,xs=np.where(m); im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); m=m[ys.min():ys.max()+1,xs.min():xs.max()+1]
    r=im.convert('RGBA'); r.putalpha(Image.fromarray((m*255).astype(np.uint8))); return r
ex=Image.open(f'{R}/mine_cart_scout/views_sheet_stern_ramp.png').convert('RGB'); W,H=ex.size
S={'dwarf':(cut(f'{R}/grimrivet_restyle/front.png'),1.5,'h','Dwarf','1.5 m tall'),
   'mc4':(cut(f'{R}/mine_cart/left.png'),7.2,'w','Mine Cart (round 4)','7.2 m'),
   'mcnew':(cut(f'{R}/mine_cart_r4_2k/v2/left.png'),7.2,'w','Mine Cart, new: turret and cargo arm','7.2 m'),
   'mc3':(cut(f'{R}/mine_cart_v3/left.png'),7.2,'w','Mine Cart v3 (being replaced)','7.2 m'),
   'exp':(cut(ex,(0,0,int(W*0.36),int(H*0.5))),7.4,'w','Explorer (science and recovery)','7.4 m'),
   'split':(cut(f'{R}/splitter/left.png'),12.7,'w','Splitter (fighter)','12.7 m'),
   'pound':(cut(f'{R}/pounder/left.png'),18.0,'w','Pounder (bomber)','18 m'),
   'wagon':(cut(f'{R}/wagon_a/left.png'),19.0,'w','Wagon','19 m'),
   'hh':(cut(f'{R}/fv_hammerhead_hq/left.png'),45.0,'w','Hammerhead (high quality, parked)','45 m'),
   'ah':(cut(f'{R}/anvilhawk_hq_flight_deck/left.png'),125.0,'w','Anvilhawk','125 m'),
   'ag':(cut(f'{R}/anvilhawk_hq/left.png'),155.0,'w','Anvilguard','155 m'),
   'bw':(cut(f'{R}/brokkrs_rest_2k/left.png'),300.0,'w',"Brokkr's Wake",'300 m')}
FT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',40)
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24); F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
WPX=3000
def lane(keys, gap_m, title, bar_m):
    span=sum(S[k][1] if S[k][2]=='w' else 1.0 for k in keys)+gap_m*(len(keys)-1)
    ppm=(WPX-140)/span
    ims=[]
    for k in keys:
        im,size,ax,name,lab=S[k]; f=ppm*size/(im.height if ax=='h' else im.width)
        ims.append((im.resize((max(2,round(im.width*f)),max(2,round(im.height*f))),Image.LANCZOS),name,lab))
    Hc=max(i.height for i,_,_ in ims)+310; c=Image.new('RGB',(WPX,Hc),(236,235,232)); g=ImageDraw.Draw(c)
    g.text((40,18),f'{title} ({ppm:.1f} px per metre)',fill=(30,30,30),font=FB)
    ground=Hc-200; x=60; ends=[-999,-999,-999]
    for im,name,lab in ims:
        c.paste(im,(x,ground-im.height),im)
        tw=max(g.textlength(name,font=F),g.textlength(lab,font=F))
        lv=next((i for i,e in enumerate(ends) if x>e+16),0)
        yy=ground+12+lv*46
        g.text((x,yy),name,fill=(30,30,30),font=F); g.text((x,yy+22),lab,fill=(90,90,90),font=F)
        ends[lv]=x+tw; x+=im.width+round(gap_m*ppm)
    g.line([(40,ground),(WPX-40,ground)],fill=(150,150,150),width=2)
    bx=WPX-60-round(bar_m*ppm); g.rectangle([bx,30,WPX-60,42],fill=(40,40,40)); g.text((bx,48),f'{bar_m:g} m',fill=(40,40,40),font=F)
    return c
L1=lane(['dwarf','mc4','mcnew','mc3','exp'],3.0,'Lane 1: the Mine Carts and the Explorer',5)
L2=lane(['dwarf','mcnew','split','pound','wagon'],4.0,'Lane 2: the small craft: fighter, bomber and the Wagon',5)
L3=lane(['dwarf','wagon','hh','ah'],8.0,'Lane 3: the Wagon to the Anvilhawk',20)
L4=lane(['mcnew','split','pound','wagon','hh','ah','ag','bw'],10.0,'Lane 4: the whole fleet at one scale',50)
top=Image.new('RGB',(WPX,90),(236,235,232)); ImageDraw.Draw(top).text((40,22),'Fleet scale: Mine Carts to Brokkr\'s Wake, true sizes',fill=(20,20,20),font=FT)
lanes=[top,L1,L2,L3,L4]; out=Image.new('RGB',(WPX,sum(l.height for l in lanes)+30),(255,255,255)); y=0
for l in lanes: out.paste(l,(0,y)); y+=l.height+10
out.save('/home/claude/driftwright-refs/views/fleet_scale/fleet_scale.png'); print(out.size)
