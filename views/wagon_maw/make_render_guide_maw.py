"""Paint-over guide, true scale: the 23.0 m Wagon (map wagon_maw) in flight, port side and front.
Head: Brokkr's Rest 2K left and front views (approved round 156), horns and guns left off, fitted to the Wagon's 5.5 x 7.8 m nose.
Body and dock: as render_guide_b (Joe's Wagon views at 1.18x, the Explorer's nose 2 m out of the stern)."""
import numpy as np
from PIL import Image, ImageDraw
exec(open('/tmp/rg/guide.py').read().split("# ---- stern view")[0])        # side view of map B: out, g, PPM, x0, ground, stern_x
K=1.18; R='/home/claude/driftwright-refs/views/brokkrs_rest_2k/'
def keyout(im,thr=40,bg=None):
    a=np.asarray(im.convert('RGB')).astype(int); bg=a[3,3] if bg is None else np.array(bg); m=np.abs(a-bg).sum(2)>thr
    r=im.convert('RGBA'); r.putalpha(Image.fromarray((m*255).astype(np.uint8))); return r
# side: her head from the left view (2304 wide): brow to the claw tips, the horn and its gun cut off above the brow
L=Image.open(R+'left.png'); s=L.width/1200
head=keyout(L.crop((int(38*s),int(178*s),int(285*s),int(615*s))))
bgc=L.convert('RGB').getpixel((5,5)); head=keyout(L.crop((int(38*s),int(178*s),int(285*s),int(615*s))),bg=bgc)
brow=int((268-178)*s)                                                          # the glowing brow band; above it the horn, cut off
top=Image.new('RGBA',(head.width,brow),(138,128,114,255)); tg=ImageDraw.Draw(top)
for yy in range(0,brow,max(8,brow//4)): tg.line([(0,yy),(head.width,yy)],fill=(176,128,64),width=4)
for xx in range(0,head.width,max(10,head.width//6)): tg.line([(xx,0),(xx,brow)],fill=(110,100,90),width=2); hd=head.copy(); hd.paste(top,(0,0)); head=hd
body_h=7.2; hp=body_h*PPM/(head.height*(470-178)/(615-178))                    # brow to maw floor = 7.2 m (0.6 m to the roof's 7.8)
head=head.resize((round(head.width*hp),round(head.height*hp)),Image.LANCZOS)
hull_top=ground-round(6.6*K*PPM)
# clear Joe's cab, then set the head on the nose
g.rectangle([x0-40,hull_top-60,x0+round(4.6*PPM),ground+10],fill=(200,200,200))
out.paste(head,(x0-round(0.6*PPM),hull_top),head)
out=out.crop((0,0,stern_x+round(2.6*PPM),out.height))
# front: Brokkr's front, horns off, fitted to 5.5 m wide x 7.2 m brow-to-maw, claws below
F=Image.open(R+'front.png'); f=F.width/1200
fr=keyout(F.crop((int(225*f),int(205*f),int(975*f),int(1110*f))),bg=F.convert('RGB').getpixel((5,5)))
fw=round(5.5*PPM); fh=round(fr.height*fw/fr.width*1.25)                        # stretched taller to the Wagon's head
fr=fr.resize((fw,fh),Image.LANCZOS)
c=Image.new('RGB',(out.width+fw+260,out.height),(200,200,200)); c.paste(out,(0,0))
c.paste(fr,(out.width+130,hull_top),fr)
c.save('/tmp/mw/guide_maw.png'); print(c.size)
