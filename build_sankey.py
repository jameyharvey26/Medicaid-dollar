import math
# ===== Medicaid Dollar-Flow Sankey, DRAFT V.4 (Public Comment) =====
W,H=2200,1110; cY=540; ys=4.4; bw=18
FED="#2f5d74"; STATE="#9bb8c4"; DOLLAR="#1a6b40"
MCO="#3f8f8a"; DUAL="#9a6fa6"; FFS="#5f7f96"
ADMIN="#9a9a9a"; MEDI="#9aa0a6"; RETAIN="#5e5e5e"; EARN="#000000"; FRAUD="#e8170f"; DUALADM="#7d6f86"
CHILD="#6fa382"; ADULT="#d8a24a"; DIS="#cf7d4f"; AGED="#6f6f9e"
INK="#272727"; MUT="#6f6f6f"; BG="#faf8f3"; LINE="#e2dccf"

# ---- ledger ($ per $100 total) ----
fed,state=64.70,35.30
admin,medicare=5.07,2.90
mco,dual,ffs=40.06,10.89,41.08
mco_ret,dual_ret,earnings,adm_marg=4.41,1.20,0.76,4.85
mco_adm,dual_adm=3.81,1.04   # adm_marg split by lane administration share (3.81+1.04=4.85)
mco_care,dual_care=35.65,9.69
order=["Long-term care","Hospitals","Other","Physicians & clinics","Behavioral health","Rx drugs"]
node={"Long-term care":28.53,"Hospitals":18.66,"Other":13.33,"Physicians & clinics":12.63,"Behavioral health":9.51,"Rx drugs":3.76}
disp={"Other":"Wrap around services"}
fraud=0.15
ffs_n={"Long-term care":19.72,"Hospitals":8.68,"Other":4.95,"Physicians & clinics":2.87,"Behavioral health":3.48,"Rx drugs":1.38}
mcoc_n={"Long-term care":6.93,"Hospitals":7.84,"Other":6.59,"Physicians & clinics":7.68,"Behavioral health":4.74,"Rx drugs":1.87}
dualc_n={"Long-term care":1.89,"Hospitals":2.14,"Other":1.79,"Physicians & clinics":2.08,"Behavioral health":1.29,"Rx drugs":0.51}
G=["Children","Adults","Disabled","Aged"]; gt={"Children":13.48,"Adults":29.56,"Disabled":24.98,"Aged":18.41}
seed={"Long-term care":[.02,.10,1.0,1.0],"Hospitals":[.85,1.0,.75,.45],"Other":[.95,.95,.80,.55],
 "Physicians & clinics":[1.05,1.0,.60,.40],"Behavioral health":[.55,1.05,1.35,.30],"Rx drugs":[.40,.85,1.05,.65]}
M={p:{g:seed[p][i] for i,g in enumerate(G)} for p in order}
for _ in range(80):
    for p in order:
        s=sum(M[p].values())
        for g in G: M[p][g]*=node[p]/s
    for g in G:
        s=sum(M[p][g] for p in order)
        for p in order: M[p][g]*=gt[g]/s
pie_frac={p:[M[p][g]/sum(M[p].values()) for g in G] for p in order}

xFED=(110,300); xSG=(300,560); xSA=(560,820); xDI=(820,1060); xPA=(1060,1300); xCL=(1300,1560); xPR=(1560,1760); xBE=(1760,2180)
svg=[]
def add(s): svg.append(s)
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def band(x0,x1,y0,y1,h0,h1,fill,op=0.82,dash=False):
    xm=(x0+x1)/2
    d=f"M{x0:.1f},{y0:.1f} C{xm:.1f},{y0:.1f} {xm:.1f},{y1:.1f} {x1:.1f},{y1:.1f} L{x1:.1f},{y1+h1:.1f} C{xm:.1f},{y1+h1:.1f} {xm:.1f},{y0+h0:.1f} {x0:.1f},{y0+h0:.1f} Z"
    da=' stroke-dasharray="5 3"' if dash else ''
    add(f'<path d="{d}" fill="{fill}" fill-opacity="{op}" stroke="{fill}" stroke-opacity="0.45" stroke-width="0.6"{da}/>')
def rect(x,y,w,h,fill,op=1.0,rx=2): add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}"/>')
def txt(x,y,s,size=13,fill=INK,anchor="start",weight="normal",halo=True,italic=False):
    it=' font-style="italic"' if italic else ''
    po=' paint-order="stroke" stroke="#faf8f3" stroke-width="2.2" stroke-linejoin="round"' if halo else ''
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{it}{po}>{esc(s)}</text>')
def lbg(x,y,s,size=12.5,anchor="start",pad=4):
    w=len(s)*size*0.56+pad*2; h=size+pad*1.5
    xx=x-pad if anchor=="start" else (x-w/2 if anchor=="middle" else x-w+pad)
    add(f'<rect x="{xx:.1f}" y="{y-size:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" fill="{BG}" fill-opacity="0.82"/>')
def fexit(x0,ytop,thick,xend,lane,color,title,sub):
    band(x0,xend,ytop,lane,thick,thick,color,0.88)
    rect(xend,lane,5,max(thick,4),color)
    lbg(xend-9,lane-5,title,13,"end"); txt(xend-9,lane-5,title,13,color,"end","bold",halo=False)
    if sub: lbg(xend-9,lane+10,sub,10.5,"end"); txt(xend-9,lane+10,sub,10.5,MUT,"end",halo=False,italic=True)
def rot_for(fracs):
    mi=max(range(len(fracs)),key=lambda i:fracs[i])
    return -90.0-(sum(fracs[:mi])+fracs[mi]/2)*360
def pie(cx,cy,r,fracs,cols,a0=-90.0):
    a=a0
    for f,c in zip(fracs,cols):
        if f<=0: continue
        a1=a+f*360
        x0=cx+r*math.cos(math.radians(a)); y0=cy+r*math.sin(math.radians(a))
        x1=cx+r*math.cos(math.radians(a1)); y1=cy+r*math.sin(math.radians(a1))
        large=1 if (a1-a)>180 else 0
        if f>=0.999:
            add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{c}"/>')
        else:
            add(f'<path d="M{cx:.1f},{cy:.1f} L{x0:.1f},{y0:.1f} A{r:.1f},{r:.1f} 0 {large},1 {x1:.1f},{y1:.1f} Z" fill="{c}" stroke="{BG}" stroke-width="1.2"/>')
        a=a1
def pielabels(cx,cy,r,fracs,a0=-90.0):
    a=a0
    for f in fracs:
        if f<=0: a+=f*360; continue
        mid=math.radians(a+f*180)
        if (r>=35 and r*f>=3.2) or (r<35 and r*f>=7.0):
            rl=r*0.60; lx=cx+rl*math.cos(mid); ly=cy+rl*math.sin(mid)+4.4
            add(f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="14" text-anchor="middle" font-weight="bold" paint-order="stroke" stroke="#3a3a3a" stroke-width="3.0" stroke-linejoin="round" fill="#ffffff">{round(f*100)}%</text>')
        else:
            rl=r+15; lx=cx+rl*math.cos(mid); ly=cy+rl*math.sin(mid)+4.0
            t0x=cx+(r+1)*math.cos(mid); t0y=cy+(r+1)*math.sin(mid); t1x=cx+(r+10)*math.cos(mid); t1y=cy+(r+10)*math.sin(mid)
            add(f'<line x1="{t0x:.1f}" y1="{t0y:.1f}" x2="{t1x:.1f}" y2="{t1y:.1f}" stroke="#555555" stroke-width="1.2"/>')
            add(f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="12.5" text-anchor="middle" font-weight="bold" paint-order="stroke" stroke="{BG}" stroke-width="2.8" stroke-linejoin="round" fill="#000000">{round(f*100)}%</text>')
        a+=f*360
add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>')
# phase headers + dividers
heads=[("FEDERAL","money from above",xFED),("STATE GOVERNMENT","fed + state in parallel",xSG),
 ("STATE AGENCY","the $100 combined",xSA),("DISBURSEMENTS","state Medicaid \u2192 3 lanes",xDI),
 ("PAYER","plan administration peeled",xPA),("CLAIMS","payers fund claims",xCL),("PROVIDERS","6 nodes, sized by spend",xPR),("BENEFICIARIES","who consumes each service",xBE)]
for name,sub,(x0,x1) in heads:
    txt(x0+6,58,name,15,INK,"start","bold",halo=False); txt(x0+6,77,sub,11.5,MUT,"start",halo=False,italic=True)
    add(f'<line x1="{x0}" y1="90" x2="{x0}" y2="918" stroke="{LINE}" stroke-width="1"/>')
add(f'<line x1="{xBE[1]}" y1="90" x2="{xBE[1]}" y2="918" stroke="{LINE}" stroke-width="1"/>')
add(f'<line x1="110" y1="90" x2="{W-20}" y2="90" stroke="{LINE}" stroke-width="1.2"/>')

# ===== sources =====
fed_top=126; st_top=655
rect(150,fed_top,bw,fed*ys,FED); rect(150,st_top,bw,state*ys,STATE)
lbg(150,fed_top-9,"Federal  $64.70",14); txt(150,fed_top-9,"Federal  $64.70",14,FED,"start","bold",halo=False)
lbg(150,st_top+state*ys+18,"State  $35.30",14); txt(150,st_top+state*ys+18,"State  $35.30",14,"#5f7f8c","start","bold",halo=False)
# trunk geometry
T0=cY-100*ys/2; TB=cY+100*ys/2
fed_lane=(T0,T0+fed*ys)
st_lane=(fed_lane[1],TB)
band(150+bw,xSG[0],fed_top,fed_lane[0],fed*ys,fed*ys,FED,0.8)
band(150+bw,xSG[0],st_top,st_lane[0],state*ys,state*ys,STATE,0.8)
band(xSG[0],xSG[1],fed_lane[0],fed_lane[0],fed*ys,fed*ys,FED,0.82)
band(xSG[0],xSG[1],st_lane[0],st_lane[0],state*ys,state*ys,STATE,0.82)
rect(xSG[0],fed_lane[0],bw,fed*ys,FED); rect(xSG[0],st_lane[0],bw,state*ys,STATE)
txt(xSG[0]+30,fed_lane[0]+fed*ys/2+4,"Federal 64.7%",13,"#ffffff","start","bold",halo=False)
txt(xSG[0]+30,st_lane[0]+state*ys/2+4,"State 35.3%",13,"#33474f","start","bold",halo=False)
# SA combined trunk, sequential peels
rect(xSA[0],T0,bw,100*ys,DOLLAR)
ax=615; mx=715
band(xSA[0]+bw,ax,T0,T0,100*ys,100*ys,DOLLAR,0.82)
top2=T0+admin*ys
band(ax,mx,top2,top2,(100-admin)*ys,(100-admin)*ys,DOLLAR,0.82)
top3=top2+medicare*ys
band(mx,xSA[1],top3,top3,(100-admin-medicare)*ys,(100-admin-medicare)*ys,DOLLAR,0.82)
fexit(ax,T0,admin*ys,xSA[1]-6,250,ADMIN,"Administration  $5.07","state / program overhead")
msY=top2+medicare*ys/2
add(f'<path d="M{mx:.1f},{msY:.1f} C{mx-120:.1f},{msY-150:.1f} 470,128 234,134" fill="none" stroke="{MEDI}" stroke-width="{medicare*ys:.1f}" stroke-opacity="0.72" stroke-linecap="round"/>')
add(f'<path d="M224,134 l16,-6 l0,12 Z" fill="{MEDI}"/>')
lbg(300,118,"Medicare premiums  $2.90",12,"start"); txt(300,118,"Medicare premiums  $2.90",12,"#5f6166","start","bold",halo=False)
lbg(300,133,"back to federal (Medicaid \u2192 Medicare)",10,"start"); txt(300,133,"back to federal (Medicaid \u2192 Medicare)",10,MUT,"start",halo=False,italic=True)
rect(xSA[1],top3,bw,(100-admin-medicare)*ys,DOLLAR)
txt((xSA[0]+xSA[1])/2+6,cY-4,"100 Dollars of",15,"#ffffff","middle","bold",halo=False)
txt((xSA[0]+xSA[1])/2+6,cY+16,"Medicaid Spending",15,"#ffffff","middle","bold",halo=False)

# ===== Disbursements =====
mco_y=top3; dual_y=mco_y+mco*ys; ffs_y=dual_y+dual*ys
peelx=1150
band(xSA[1]+bw,peelx,mco_y,mco_y,mco*ys,mco*ys,MCO,0.82)
band(xSA[1]+bw,peelx,dual_y,dual_y,dual*ys,dual*ys,DUAL,0.82)
band(xSA[1]+bw,xCL[0],ffs_y,ffs_y,ffs*ys,ffs*ys,FFS,0.82)
rect(xDI[0],mco_y,bw,mco*ys,MCO); rect(xDI[0],dual_y,bw,dual*ys,DUAL); rect(xDI[0],ffs_y,bw,ffs*ys,FFS)
lbg(xDI[0]+24,mco_y+mco*ys/2+5,"MCO capitation  $40.06",13); txt(xDI[0]+24,mco_y+mco*ys/2+5,"MCO capitation  $40.06",13,"#1f5b57","start","bold",halo=False)
lbg(xDI[0]+24,dual_y+dual*ys/2+5,"Dual MCO capitation  $10.89",13); txt(xDI[0]+24,dual_y+dual*ys/2+5,"Dual MCO capitation  $10.89",13,"#5a3d63","start","bold",halo=False)
lbg(xDI[0]+24,ffs_y+ffs*ys/2+5,"Fee-for-service  $41.08",13); txt(xDI[0]+24,ffs_y+ffs*ys/2+5,"Fee-for-service  $41.08",13,"#36505f","start","bold",halo=False)

# ===== Payer: peel administration, fork into earnings + MCO admin + dual-MCO admin =====
mco_care_y=mco_y+mco_ret*ys; dual_care_y=dual_y+dual_ret*ys
band(peelx,xCL[0],mco_care_y,mco_care_y,mco_care*ys,mco_care*ys,MCO,0.82)
band(peelx,xCL[0],dual_care_y,dual_care_y,dual_care*ys,dual_care*ys,DUAL,0.82)
plx=1235; planY=250
band(peelx,plx,mco_y,planY,mco_ret*ys,mco_ret*ys,RETAIN,0.88)
band(peelx,plx,dual_y,planY+mco_ret*ys,dual_ret*ys,dual_ret*ys,RETAIN,0.88)
yk=planY
band(plx,xPA[1]-6,yk,136,earnings*ys,earnings*ys,EARN,0.9); yk+=earnings*ys
rect(xPA[1]-6,136,5,max(earnings*ys,4),EARN)
lbg(xPA[1]-15,132,"Public-company earnings  $0.76",13,"end"); txt(xPA[1]-15,132,"Public-company earnings  $0.76",13,EARN,"end","bold",halo=False)
lbg(xPA[1]-15,148,"subset of margin (est.)",10.5,"end"); txt(xPA[1]-15,148,"subset of margin (est.)",10.5,MUT,"end",halo=False,italic=True)
band(plx,xPA[1]-6,yk,198,mco_adm*ys,mco_adm*ys,RETAIN,0.9); yk+=mco_adm*ys
rect(xPA[1]-6,198,5,mco_adm*ys,RETAIN)
lbg(xPA[1]-15,194,"MCO plan administration  $3.81",13,"end"); txt(xPA[1]-15,194,"MCO plan administration  $3.81",13,RETAIN,"end","bold",halo=False)
lbg(xPA[1]-15,210,"non-dual MCO administration",10.5,"end"); txt(xPA[1]-15,210,"non-dual MCO administration",10.5,MUT,"end",halo=False,italic=True)
band(plx,xPA[1]-6,yk,262,dual_adm*ys,dual_adm*ys,DUALADM,0.92); yk+=dual_adm*ys
rect(xPA[1]-6,262,5,max(dual_adm*ys,4),DUALADM)
lbg(xPA[1]-15,258,"Dual MCO plan administration  $1.04",13,"end"); txt(xPA[1]-15,258,"Dual MCO plan administration  $1.04",13,DUALADM,"end","bold",halo=False)
lbg(xPA[1]-15,274,"dual-plan administration",10.5,"end"); txt(xPA[1]-15,274,"dual-plan administration",10.5,MUT,"end",halo=False,italic=True)

# ===== CLAIMS: 3 care lanes fan into 6 provider bars =====
gg=50; htot=sum(node[p] for p in order)*ys+(len(order)-1)*gg; ntop=cY-htot/2
node_y={}; y=ntop
for p in order: node_y[p]=y; y+=node[p]*ys+gg
barL=xPR[0]; barW=140; barR=barL+barW
lane_src={"MCO":mco_care_y,"Dual":dual_care_y,"FFS":ffs_y}
comp={"MCO":mcoc_n,"Dual":dualc_n,"FFS":ffs_n}; lc={"MCO":MCO,"Dual":DUAL,"FFS":FFS}
ncur={p:node_y[p] for p in order}
fh=max(fraud*ys,3.0)
add(f'<path d="M{xCL[0]+6:.1f},{ffs_y+ffs*ys-fh/2:.1f} C{xCL[0]+110:.1f},{ffs_y+ffs*ys:.1f} {xCL[1]-80:.1f},860 {xCL[1]-54:.1f},876" fill="none" stroke="{FRAUD}" stroke-width="{fh:.1f}" stroke-opacity="0.95" stroke-linecap="round"/>')
rect(xCL[1]-54,872,6,max(fh,5),FRAUD)
lbg(xCL[1]-44,870,"Documented fraud  $0.15",12,"start"); txt(xCL[1]-44,870,"Documented fraud  $0.15",12,FRAUD,"start","bold",halo=False)
lbg(xCL[1]-44,884,"true loss, mostly fee-for-service (not to scale)",9.5,"start"); txt(xCL[1]-44,884,"true loss, mostly fee-for-service (not to scale)",9.5,MUT,"start",halo=False,italic=True)
for p in order:
    for L in ["MCO","Dual","FFS"]:
        v=comp[L][p]; h=v*ys
        band(xCL[0],barL,lane_src[L],ncur[p],h,h,lc[L],0.62 if L!="FFS" else 0.8, dash=(L!="FFS"))
        lane_src[L]+=h; ncur[p]+=h
# ===== PROVIDERS =====
for p in order:
    yy=node_y[p]
    for L,val in [("MCO",mcoc_n[p]),("Dual",dualc_n[p]),("FFS",ffs_n[p])]:
        rect(barL,yy,barW,val*ys,lc[L]); yy+=val*ys
    nm=disp.get(p,p)+("*" if p=="Other" else "")
    lbg(barL+barW/2,node_y[p]-9,f"{nm}  ${node[p]:.2f}",13.5,"middle"); txt(barL+barW/2,node_y[p]-9,f"{nm}  ${node[p]:.2f}",13.5,INK,"middle","bold",halo=False)
# ===== BENEFICIARIES: two staggered columns; each pie aligned to its bar's centre =====
xLcol=1885; xRcol=2090
for i,p in enumerate(order):
    cx=xLcol if i%2==0 else xRcol
    cy=node_y[p]+node[p]*ys/2; r=16.8*math.sqrt(node[p]); a0=rot_for(pie_frac[p])
    if p=="Rx drugs": a0+=30   # nudge so the small outside labels clear the $ below
    pie(cx,cy,r,pie_frac[p],[CHILD,ADULT,DIS,AGED],a0)
    pielabels(cx,cy,r,pie_frac[p],a0)
    nm=disp.get(p,p)+("*" if p=="Other" else "")
    lbg(cx,cy-r-10,nm,19.5,"middle"); txt(cx,cy-r-10,nm,19.5,INK,"middle","bold",halo=False)
    lbg(cx,cy+r+22,f"${node[p]:.2f}",19.5,"middle"); txt(cx,cy+r+22,f"${node[p]:.2f}",19.5,INK,"middle","bold",halo=False)

# beneficiary legend (compact, horizontal)
lx=xBE[0]+20; ly=108
txt(lx,ly,"Share of each service consumed by:",12.5,INK,"start","bold",halo=False)
gx=lx
for g,c in zip(G,[CHILD,ADULT,DIS,AGED]):
    rect(gx,ly+11,13,13,c); txt(gx+18,ly+21,g,12,INK,"start",halo=False)
    gx+=40+len(g)*12*0.55
txt(lx,ly+42,"numbers = % of that node's dollars (black sits outside)",10.5,MUT,"start",halo=False,italic=True)

# ===== BOTTOM TRACKER: running balance of the $100 (fonts 2x) =====
add(f'<line x1="110" y1="918" x2="{W-20}" y2="918" stroke="{LINE}" stroke-width="1.2"/>')
by=1012
cps=[(560,"$100.00",["$100 Medicaid","Dollars"]),(820,"$92.03",["Disbursed"]),(1300,"$86.42",["Claims paid"]),(1560,"$86.27",["Health Services","delivered"])]
deltas=[(690,"\u2212$7.97"),(1060,"\u2212$5.61"),(1430,"\u2212$0.15")]
add(f'<line x1="{cps[0][0]}" y1="{by}" x2="{cps[-1][0]}" y2="{by}" stroke="{DOLLAR}" stroke-width="4.8" stroke-opacity="0.5"/>')
for x,val,lab in cps:
    add(f'<circle cx="{x}" cy="{by}" r="11" fill="{DOLLAR}"/>')
    txt(x,by-24,val,36,DOLLAR,"middle","bold",halo=False)
    for j,ln in enumerate(lab):
        txt(x,by+46+j*30,ln,25,INK,"middle","bold",halo=False)
for x,d in deltas:
    txt(x,by-24,d,24,FRAUD,"middle","bold",halo=False)

SVG=f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg">\n'+"\n".join(svg)+"\n</svg>"
leg=[(FED,"Federal"),(STATE,"State"),(DOLLAR,"Medicaid dollar (state agency)"),(MCO,"MCO capitation"),(DUAL,"Dual MCO capitation"),(FFS,"Fee-for-service"),
 (ADMIN,"Administration (out)"),(MEDI,"Medicare premiums (back to federal)"),(RETAIN,"MCO plan administration (out)"),(DUALADM,"Dual MCO plan administration (out)"),(EARN,"Public-company earnings (out)"),(FRAUD,"Documented fraud (out)")]
legh="".join([f'<span class="lg"><span class="sw" style="background:{c}"></span>{t}</span>' for c,t in leg])
HTML=f'''<!doctype html><html><head><meta charset="utf-8"><title>$100 Medicaid Dollars</title>
<style>
 body{{margin:0;background:{BG};font-family:'Segoe UI',Helvetica,Arial,sans-serif;color:{INK}}}
 .wrap{{max-width:1380px;margin:0 auto;padding:24px 28px 40px}}
 .draft{{display:inline-block;background:{FRAUD};color:#fff;font-weight:700;font-size:12px;letter-spacing:.12em;padding:4px 10px;border-radius:3px}}
 h1{{font-size:30px;margin:13px 0 4px}} .sub{{color:{MUT};font-size:15px;margin:0 0 2px;max-width:1050px}}
 .meta{{color:{MUT};font-size:12.5px;font-style:italic;margin:2px 0 12px}}
 .legend{{margin:6px 0 2px;font-size:12.5px}} .lg{{display:inline-block;margin:0 15px 6px 0}}
 .sw{{display:inline-block;width:13px;height:13px;border-radius:3px;vertical-align:-2px;margin-right:5px}}
 .fn{{font-size:12px;color:{MUT};line-height:1.55;margin-top:16px;border-top:1px solid {LINE};padding-top:12px}} .fn b{{color:#444}}
</style></head><body><div class="wrap">
<div><span class="draft">DRAFT V.4 &mdash; PUBLIC COMMENT</span></div>
<h1>$100 Medicaid Dollars</h1>
<p class="sub">$100 is the combined federal + state dollar. It comes together at the state, runs through the agency, is disbursed across three payer lanes, funds <b>claims</b> that fan out to six <b>providers</b> &mdash; then read as the share of each service consumed by each eligibility group. The tracker along the bottom follows the running balance as losses peel off. FY2024.</p>
<p class="meta">Per $100 of total Medicaid spending &middot; width = dollars &middot; admin, Medicare premiums (returned to the federal government), plan administration and fraud peel off, leaving $86.42 at providers and $86.27 of health services delivered &middot; pies (right) are sized to each provider bar and show who consumes that service.</p>
<div class="legend">{legh}</div>
{SVG}
<div class="fn">
<p style="margin:0 0 11px;font-style:italic;color:#444;font-size:12.5px"><b>*Wrap around services</b> include labs, imaging, equipment, dental, screening, transportation and hospice.</p>
<b>Reading it.</b> Federal ($64.70) enters from above and merges with state ($35.30) into the $100 Medicaid dollar at the state agency. Two losses peel there: <b>administration</b> ($5.07) and <b>Medicare premiums for duals</b> ($2.90), which curve back left to the federal government (Medicaid paying Medicare). The remaining $92.03 is disbursed across <b>MCO</b>, <b>dual-MCO</b> and <b>fee-for-service</b> lanes. In the payer phase the capitated lanes give up <b>$5.61</b> to plan administration and earnings (plan administration $4.85 &mdash; $3.81 non-dual MCO + $1.04 dual-MCO &mdash; plus public-company earnings $0.76, a subset). What remains ($86.42) funds <b>claims</b>, which fan out to six <b>provider</b> bars (sized by spend, layered by payer source); <b>documented fraud</b> ($0.15) peels off the bottom of the fee-for-service lane, leaving $86.27 of health services delivered. Each provider bar ends in a pie, sized to the bar, showing who consumes that service.<br><br>
<b>Conservation:</b> 100 &rarr; &minus;5.07 admin = 94.93 &rarr; &minus;2.90 Medicare = 92.03 (= MCO 40.06 + dual 10.89 + FFS 41.08) &rarr; &minus;5.61 plan admin &amp; earnings = 86.42 to providers (node sum 86.43) &rarr; &minus;0.15 fraud = 86.27 delivered. Every cut balances.<br><br>
<b>Draft notes.</b> (1) <b>FQHCs are merged into "Physicians &amp; clinics"</b> &mdash; the FFS FQHC line is real but MCO FQHC dollars sit unlabelled inside the capitated "professional" bucket, so a standalone FQHC node would understate it. (2) <b>Behavioral health (~$9.51, ~11% of service dollars; literature 9.3&ndash;13%)</b> is broken out as its own node from every line it occupies. The cross-line split is an estimate; T-MSIS claims would refine it. (3) <b>"Wrap around services" ($13.33)</b>, now net of behavioral health, = dental + the CMS-64 "other acute" catch-all (NEMT, DME, lab/imaging, therapies, EPSDT/preventive, hospice, etc.); not itemised in the source. (4) Provider order is true size. (5) Plan administration $4.85 is split by lane in proportion to each lane's share ($3.81 non-dual MCO + $1.04 dual-MCO); public-company earnings ($0.76) is a subset of margin, estimated pending 10-K allocation. (6) Beneficiary pies are IPF-balanced to each service's user mix and to group totals &mdash; a re-expression of provider dollars, not a measured flow. (7) Dual capitation (~$10.89) is the softest payer figure. (8) Vintages: CMS-64 FY2024, HMA mix CY2021, group shares FY2023, duals CY2022.
</div>
</div></body></html>'''
open("/home/claude/medicaid_dollar_sankey.html","w").write(HTML)
open("/home/claude/medicaid_dollar_sankey.svg","w").write(SVG)
print("wrote v3")
