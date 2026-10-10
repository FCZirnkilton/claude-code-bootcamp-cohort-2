from PIL import Image, ImageDraw, ImageFont
import random
random.seed(7)
W,H=1600,1110
im=Image.new("RGB",(W,H),"#fbfaf6"); d=ImageDraw.Draw(im)
F="/usr/share/fonts/truetype/dejavu/"
hand=ImageFont.truetype(F+"DejaVuSans.ttf",26); bold=ImageFont.truetype(F+"DejaVuSans-Bold.ttf",30)
small=ImageFont.truetype(F+"DejaVuSans.ttf",20); note=ImageFont.truetype(F+"DejaVuSansMono-Oblique.ttf",20)
ink="#2b2b2b"; red="#c0392b"; blue="#2c5aa0"
def wob(box,w=3,r=10):
    x0,y0,x1,y1=box
    r=min(r,(y1-y0)//2-4)
    for k in range(2):
        j=lambda: random.uniform(-2.2,2.2)
        d.rounded_rectangle((x0+j(),y0+j(),x1+j(),y1+j()),r,outline=ink,width=w)
def text(xy,s,f=hand,c=ink): d.text(xy,s,font=f,fill=c)
wob((40,30,W-40,130)); text((70,50),"SHIPYARD",small); text((70,78),"Release v1.4 readiness",bold)
wob((W-330,60,W-70,104),r=22); text((W-310,68),"Target date",small)
labels=["Open tasks","Completed","Overdue","Notes"]
cw=(W-80-3*30)/4
for i,l in enumerate(labels):
    x=40+i*(cw+30); wob((x,160,x+cw,290)); text((x+24,180),l.upper(),small); text((x+24,215),"##",bold,red if i==2 else ink)
wob((40,330,W-40,700)); text((70,350),"Release tasks",bold)
wob((W-560,346,W-330,390),r=8); text((W-545,355),"Owner  v",small)
wob((W-310,346,W-70,390),r=8); text((W-295,355),"Status: pending v",small)
cols=[70,760,1000,1260]
for c,h in zip(cols,["TASK","OWNER","DUE","STATUS"]): text((c,415),h,small)
d.line((60,448,W-60,448),fill=ink,width=2)
for r in range(4):
    y=465+r*45
    text((cols[0],y),"———————————",small); text((cols[1],y),"name",small)
    text((cols[2],y),"yyyy-mm-dd",small,red if r<2 else ink); wob((cols[3],y-4,cols[3]+110,y+28),w=2,r=14); text((cols[3]+18,y),"pending",small)
wob((40,740,W-40,1050)); text((70,760),"Engineering notes",bold)
wob((W-480,756,W-70,802),r=8); text((W-465,766),"Search notes...",small,"#777")
for i,t in enumerate(["#ops","#backend","#qa","#release:v1.4"]):
    x=70+i*215; wob((x,820,x+195,858),w=2,r=18); text((x+18,826),t,small)
for i in range(2):
    y=875+i*85; wob((70,y,W-70,y+72),w=2)
    text((90,y+8),"Note title",hand); text((90,y+40),"first line of body ...   #tag #tag",small,"#666")
d.text((60,300),"4 KPI cards across on desktop, 2x2 on phones. Overdue = pending + past due (red).",font=note,fill=blue)
d.text((60,660),"Filters combine (owner AND status). Default: pending. Empty state message. Overdue dates red.",font=note,fill=blue)
d.text((60,708),"Phones (<760px): table rows become stacked cards; filters stack vertically.",font=note,fill=blue)
d.text((60,1065),"Tag chip click = filter, click again = clear. Search: title + body. Data: GET /api/tasks, GET /api/notes",font=note,fill=blue)
im.save("release-dashboard.png"); print(im.size)
