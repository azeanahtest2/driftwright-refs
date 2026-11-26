import numpy as np
from PIL import Image, ImageDraw, ImageFont
R='/home/claude/driftwright-refs/views'
def cut(img, box=None):
    im=Image.open(img).convert('RGB') if isinstance(img,str) else img
    if box: im=im.crop(box)
    a=np.asarray(im).astype(int); bg=a[3,3]; m=np.abs(a-bg).sum(2)>36
    ys,xs=np.where(m); im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); m=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
    r=im.convert('RGBA'); r.putalpha(Image.fromarray((m*255).astype(np.uint8))); return r
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24); F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19); FS=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
wag=cut(f'{R}/wagon_a/left.png')                     # 19 m, bow left
exs=Image.open('/tmp/mc/explorer_views.png').convert('RGB'); W,H=exs.size
exp=cut(exs,(0,0,int(W*0.40),int(H*0.5)))           # 7.4 m, bow left
def flatbed_wagon(ppm):
    """The approved Wagon's front section at 1.18x, an 11.4 m bed behind it, the Explorer on the bed."""
    k=ppm*19.0*1.18/wag.width; w=wag.resize((round(wag.width*k),round(wag.height*k)),Image.LANCZOS)
    cutx=round(w.width*1090/1594); front=w.crop((0,0,cutx,w.height))
    bedL=round(11.4*ppm); Wt=cutx+bedL
    eng=w.crop((round(w.width*1240/1594),round(w.height*335/526),w.width,round(w.height*468/526)))   # the approved engine, as drawn
    img=Image.new('RGBA',(Wt,w.height),(0,0,0,0)); img.paste(front,(0,0),front)
    g=ImageDraw.Draw(img)
    deck_top=round(w.height*0.55); deck_bot=round(w.height*0.70)
    g.rectangle([cutx,deck_top,Wt-1,deck_bot],fill=(70,72,80,255),outline=(150,120,60,255),width=3)
    for x in range(cutx,Wt,round(ppm*1.0)): g.polygon([(x,deck_top),(x+round(ppm*0.5),deck_top),(x+round(ppm*0.3),deck_top+round(ppm*0.35)),(x-round(ppm*0.2),deck_top+round(ppm*0.35))],fill=(200,160,40,255))
    rail=round(ppm*1.0); g.line([(cutx,deck_top-rail),(Wt-1,deck_top-rail)],fill=(150,120,60,255),width=3)
    for x in range(cutx,Wt,round(ppm*1.5)): g.line([(x,deck_top-rail),(x,deck_top)],fill=(150,120,60,255),width=3)
    img.paste(eng,(Wt-eng.width,deck_bot-round(eng.height*0.1)),eng)
    ke=ppm*7.4/exp.width; e=exp.resize((round(exp.width*ke),round(exp.height*ke)),Image.LANCZOS)
    ex=cutx+round(2.0*ppm); img.paste(e,(ex,deck_top-e.height),e)
    return img, cutx, ex, e.width, deck_top
items=[('Dwarf',cut(f'{R}/grimrivet_restyle/front.png'),1.38,'h','1.4 m tall'),
 ('Mine Cart v3',cut(f'{R}/mine_cart_v3/left.png'),7.2,'w','7.2 m'),
 ('Mine Cart Explorer',exp,7.4,'w','about 7.4 m'),
 ('Wagon (approved)',wag,19.0,'w','19 m x 7.1 m x 6.6 m'),
 ('Flatbed Wagon (guide)',None,26.7,'w','about 26.7 m x 8.4 m x 7.8 m'),
 ('Hammerhead',cut(f'{R}/fv_hammerhead_cutter_flight/left.png'),45.0,'w','45 m')]
Wpx=2800; gap=4.0; tot=sum(s for _,_,s,a,_ in items if a=='w')+1.0+gap*5; ppm=(Wpx-120)/tot
row=[]
for n,im,s,a,lab in items:
    if im is None: im,_,_,_,_=flatbed_wagon(ppm)
    else:
        k=ppm*s/(im.height if a=='h' else im.width); im=im.resize((max(1,round(im.width*k)),max(1,round(im.height*k))),Image.LANCZOS)
    row.append((n,im,lab))
Hr=max(i.height for _,i,_ in row)+190
# the detail panel: the flatbed Wagon large, with dimensions
ppm2=(Wpx-300)/26.7; fw,cutx,ex,ew,dt=flatbed_wagon(ppm2)
Hd=fw.height+230
out=Image.new('RGB',(Wpx,Hr+Hd),(234,234,232)); g=ImageDraw.Draw(out)
g.text((20,12),'True scale, dwarf to Hammerhead (approved side views)',fill=(35,35,35),font=FB)
ground=Hr-120; x=40; last=-1; lvl=0
for n,im,lab in row:
    out.paste(im,(x,ground-im.height),im)
    tw=max(g.textlength(n,font=F),g.textlength(lab,font=F))+14
    lvl=(lvl+1)%2 if x<last else 0; y=ground+8+lvl*50
    if lvl: g.line([(x+im.width//2,ground+2),(x+im.width//2,y-2)],fill=(150,150,150))
    g.text((x,y),n,fill=(30,30,30),font=F); g.text((x,y+23),lab,fill=(95,95,95),font=F); last=x+tw
    x+=im.width+round(gap*ppm)
g.line([(20,ground),(Wpx-20,ground)],fill=(150,150,150),width=2)
L=round(10*ppm); g.rectangle([Wpx-60-L,22,Wpx-60,32],fill=(60,60,60)); g.text((Wpx-60-L,36),'10 m',fill=(60,60,60),font=F)
# detail
oy=Hr; g.line([(0,oy),(Wpx,oy)],fill=(200,200,200),width=2)
g.text((20,oy+12),'The flatbed Wagon, enlarged: the approved front section at 1.18x, an 11.4 m bed, the Explorer with 2 m clear fore and aft',fill=(35,35,35),font=FB)
bx=150; gy=oy+70+fw.height
out.paste(fw,(bx,gy-fw.height),fw)
def dim(x0,x1,y,txt):
    g.line([(x0,y),(x1,y)],fill=(40,40,40),width=2); g.line([(x0,y-8),(x0,y+8)],fill=(40,40,40),width=2); g.line([(x1,y-8),(x1,y+8)],fill=(40,40,40),width=2)
    tw=g.textlength(txt,font=FS); g.text(((x0+x1)/2-tw/2,y+6),txt,fill=(40,40,40),font=FS)
dim(bx,bx+cutx,gy+30,'cab and living section about 15.3 m (57%)')
dim(bx+cutx,bx+fw.width,gy+30,'bed 11.4 m (43%)')
dim(bx+cutx,bx+ex,gy+80,'2 m'); dim(bx+ex,bx+ex+ew,gy+80,'Explorer 7.4 m'); dim(bx+ex+ew,bx+fw.width,gy+80,'2 m')
dim(bx,bx+fw.width,gy+130,'overall about 26.7 m')
g.text((bx,gy+165),'Across the bed (not shown): 7.4 m inside the rails = 1.5 m + Explorer 4.4 m + 1.5 m; hull 8.4 m outside. Height about 7.8 m (the approved 6.6 m at 1.18x). Bed rails and engine are placeholders for the design; the cargo arm is not drawn.',fill=(40,40,40),font=F)
g.line([(bx,gy),(bx+fw.width,gy)],fill=(150,150,150),width=2)
out.save('/tmp/sc/true_scale_guide.png'); print(out.size)
