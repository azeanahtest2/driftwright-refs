import numpy as np
from PIL import Image, ImageDraw, ImageFont
R='/home/claude/driftwright-refs/views'
def cut(img, box=None):
    im=Image.open(img).convert('RGB') if isinstance(img,str) else img
    if box: im=im.crop(box)
    a=np.asarray(im).astype(int); bg=a[3,3]; m=np.abs(a-bg).sum(2)>36
    ys,xs=np.where(m); im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    m=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
    rgba=im.convert('RGBA'); al=Image.fromarray((m*255).astype(np.uint8)); rgba.putalpha(al); return rgba
exp_sheet=Image.open('/tmp/mc/explorer_views.png').convert('RGB'); W,H=exp_sheet.size
items=[  # name, image, size along the measured axis (m), axis, label
 ('Dwarf', cut(f'{R}/grimrivet_restyle/front.png'), 1.38, 'h', '1.4 m tall'),
 ('Mine Cart v3', cut(f'{R}/mine_cart_v3/left.png'), 7.2, 'w', '7.2 m'),
 ('Mine Cart Explorer', cut(exp_sheet, (0,0,int(W*0.40),int(H*0.5))), 7.4, 'w', 'about 7.4 m'),
 ('Wagon (approved)', cut(f'{R}/wagon_a/left.png'), 19.0, 'w', '19 m'),
 ('Wagon, scaled 1.65x', cut(f'{R}/wagon_a/left.png'), 31.0, 'w', 'about 31 m'),
 ('Hammerhead', cut(f'{R}/fv_hammerhead_cutter_flight/left.png'), 45.0, 'w', '45 m'),
 ('Anvilhawk', cut(f'{R}/anvilhawk_hq_flight_deck/left.png'), 125.0, 'w', '125 m'),
]
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22); F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
def row(sel, ppm, gap_m, title, Wpx):
    ims=[]
    for n,im,size,ax,lab in sel:
        k=ppm*size/(im.height if ax=='h' else im.width); ims.append((n,im.resize((max(1,round(im.width*k)),max(1,round(im.height*k))),Image.LANCZOS),lab))
    Hc=max(i.height for _,i,_ in ims)+170
    c=Image.new('RGB',(Wpx,Hc),(232,232,230)); g=ImageDraw.Draw(c)
    g.text((20,10),title,fill=(40,40,40),font=FB)
    ground=Hc-110; x=40; last=-1; lvl=0
    for n,im,lab in ims:
        c.paste(im,(x,ground-im.height),im)
        tw=max(g.textlength(n,font=F),g.textlength(lab,font=F))+12
        lvl = (lvl+1)%2 if x < last else 0
        y=ground+8+lvl*48
        if lvl: g.line([(x+im.width//2,ground+2),(x+im.width//2,y-2)],fill=(150,150,150),width=1)
        g.text((x,y),n,fill=(30,30,30),font=F); g.text((x,y+22),lab,fill=(90,90,90),font=F)
        last=x+tw
        x+=im.width+round(gap_m*ppm)
    g.line([(20,ground),(Wpx-20,ground)],fill=(150,150,150),width=2)
    # scale bar 10 m
    L=round(10*ppm); g.rectangle([Wpx-60-L,20,Wpx-60,30],fill=(60,60,60)); g.text((Wpx-60-L,34),'10 m',fill=(60,60,60),font=F)
    return c
Wpx=2600
tot=sum(s for _,_,s,ax,_ in items if ax=='w')+1.0+6*8
r1=row(items,(Wpx-120)/tot,8,'All to one scale',Wpx)
small=items[:5]; tot2=sum(s for _,_,s,ax,_ in small if ax=='w')+1.0+4*3
r2=row(small,(Wpx-120)/tot2,3,'The smaller craft, enlarged (same scale as each other)',Wpx)
out=Image.new('RGB',(Wpx,r1.height+r2.height),(232,232,230)); out.paste(r1,(0,0)); out.paste(r2,(0,r1.height))
out.save('/tmp/sc/scale_lineup.png'); print(out.size)
