"""Exact-scale guide for the Wagon (1.18x, 23.0 m, dock trimmed to hull width) with the Mine Cart Explorer docked as her tail gun, nose 2 m out.
Port side (nose left) and stern view. Sources: Joe's Wagon views (uploads wagon_port_side, wagon_back), the Explorer stern-ramp sheet."""
import numpy as np
from PIL import Image, ImageDraw
K=1.18
def cut(im,thr=36):
    a=np.asarray(im.convert('RGB')).astype(int); bg=a[3,3]; m=np.abs(a-bg).sum(2)>thr; ys,xs=np.where(m)
    im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).convert('RGBA'); m=m[ys.min():ys.max()+1,xs.min():xs.max()+1]
    im.putalpha(Image.fromarray((m*255).astype(np.uint8))); return im
ws=cut(Image.open('/tmp/mc/wagon_port_side.png')); wb=cut(Image.open('/tmp/mc/wagon_back.png'))
ex=Image.open('/tmp/rmp/explorer_ramp.png').convert('RGB'); W,H=ex.size
ex_side=cut(ex.crop((int(W*0.62),0,W,int(H*0.5))))          # her starboard, bow right
ex_front=cut(ex.crop((int(W*0.4),0,int(W*0.62),int(H*0.5))))
BG=(200,200,200); out=Image.new('RGB',(2304,1296),BG)
# ---- port side: Joe's Wagon is 19 m nose to engine; scaled 1.18 -> 22.4 m; the body forward of the bay = nose -9.6 .. +3.6 m
PPM=58
ws_len=19.0*K; s=ws_len*PPM/ws.width; ws2=ws.resize((round(ws.width*s),round(ws.height*s)),Image.LANCZOS)
fwd_m=(3.6+9.6)*K; fwd_px=round(fwd_m*PPM)
x0,ground=90,980
front=ws2.crop((0,0,fwd_px,ws2.height)); aft=ws2.crop((fwd_px,0,ws2.width,ws2.height))
out.paste(front,(x0,ground-ws2.height),front)
# the dock module: the old bay and engine stretched to 7.4 m of hull (23.0 m overall)
dock_m=23.0-fwd_m; aft2=aft.resize((round(aft.width*(dock_m*PPM)/(aft.width*0.80)),aft.height),Image.LANCZOS)  # box is ~80% of the aft crop, engine juts past
out.paste(aft2,(x0+fwd_px,ground-ws2.height),aft2)
stern_x=x0+round(23.0*PPM)
# the Explorer: 7.4 m long, her bow 2 m past the stern, on the dock deck 3.0*K above the ground
es=EXL=7.4*PPM/ex_side.width; e2=ex_side.resize((round(ex_side.width*es),round(ex_side.height*es)),Image.LANCZOS)
deck_y=ground-round(3.0*K*PPM)
top=max(0,e2.height-round(3.8*PPM)); nose=e2.crop((e2.width-round(2.0*PPM),top,e2.width,e2.height))
out.paste(nose,(stern_x,deck_y-nose.height),nose)
g=ImageDraw.Draw(out)
g.rectangle([stern_x-10,deck_y-round(4.2*PPM),stern_x+6,deck_y+6],fill=(190,110,40),outline=(90,50,20),width=3)  # gasket collar
# ---- stern view: 7.1 m wide x 6.6 m tall scaled
bx0,bground=1660,980; bp=(6.6*K*PPM)/wb.height
wb2=wb.resize((round(wb.width*bp),round(wb.height*bp)),Image.LANCZOS); out.paste(wb2,(bx0,bground-wb2.height),wb2)
ppm_b=wb2.height/(6.6*K)
fe=4.4*ppm_b/ex_front.width; f2=ex_front.resize((round(ex_front.width*fe),round(ex_front.height*fe)),Image.LANCZOS); f2=f2.crop((0,max(0,f2.height-round(3.8*ppm_b)),f2.width,f2.height))
cx=bx0+wb2.width//2; bdeck=bground-round(3.0*K*ppm_b)
g.rounded_rectangle([cx-f2.width//2-22,bdeck-f2.height-22,cx+f2.width//2+22,bdeck+14],radius=40,fill=(190,110,40),outline=(90,50,20),width=4)
g.rounded_rectangle([cx-f2.width//2-6,bdeck-f2.height-6,cx+f2.width//2+6,bdeck+2],radius=30,fill=(40,36,34))
out.paste(f2,(cx-f2.width//2,bdeck-f2.height),f2)
out.save('/tmp/rg/guide.png'); print(stern_x, out.size)
