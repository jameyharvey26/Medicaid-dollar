import math
# ===== Medicaid Dollar-Flow Sankey, DRAFT V.4 (Public Comment) =====
W,H=2200,1240; cY=540; ys=4.4; bw=18
FED="#2f5d74"; STATE="#9bb8c4"; DOLLAR="#1a6b40"
MCO="#3f8f8a"; DUAL="#9a6fa6"; FFS="#5f7f96"
ADMIN="#9a9a9a"; MEDI="#9aa0a6"; RETAIN="#5e5e5e"; EARN="#000000"; FRAUD="#e8170f"; DUALADM="#7d6f86"
CHILD="#6fa382"; ADULT="#d8a24a"; DIS="#cf7d4f"; AGED="#6f6f9e"
INK="#272727"; MUT="#6f6f6f"; BG="#faf8f3"; LINE="#e2dccf"



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

order=["Long-term care","Hospitals","Other","Physicians & clinics","Behavioral health","Rx drugs"]
disp={"Other":"Wrap around services"}
G=["Children","Adults","Disabled","Aged"]
seed={"Long-term care":[.02,.10,1.0,1.0],"Hospitals":[.85,1.0,.75,.45],"Other":[.95,.95,.80,.55],
 "Physicians & clinics":[1.05,1.0,.60,.40],"Behavioral health":[.55,1.05,1.35,.30],"Rx drugs":[.40,.85,1.05,.65]}


def render(cfg):
    """Draw one instance. cfg is an Instance from instances.py."""
    global svg
    svg = []
    fed, state, admin, medicare, mco, dual, ffs, mco_ret, dual_ret, earnings, adm_marg, mco_adm, dual_adm, mco_care, dual_care, node, fraud, ffs_n, mcoc_n, dualc_n, gt = (
        cfg.fed, cfg.state, cfg.admin, cfg.medicare, cfg.mco, cfg.dual, cfg.ffs, cfg.mco_ret, cfg.dual_ret, cfg.earnings, cfg.adm_marg, cfg.mco_adm, cfg.dual_adm, cfg.mco_care, cfg.dual_care, cfg.node, cfg.fraud, cfg.ffs_n, cfg.mcoc_n, cfg.dualc_n, cfg.gt)
    order = cfg.order
    disp = cfg.disp
    # ABSENT DATA IS ABSENT (S-071). A missing lane or column is omitted and
    # declared, never estimated from a national share (S-068).
    pie_frac = _solve_pies(order, node, gt) if cfg.show_beneficiaries else None
    add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>')
    # phase headers + dividers
    heads=[("FEDERAL","money from above",xFED),("STATE GOVERNMENT","fed + state in parallel",xSG),
     ("STATE AGENCY","the $100 combined",xSA),("DISBURSEMENTS","state Medicaid \u2192 3 lanes",xDI),
     ("PAYER","plan administration peeled",xPA),("CLAIMS","payers fund claims",xCL),("PROVIDERS",f"{len(cfg.order)} nodes, sized by spend",xPR)]
    if cfg.show_beneficiaries:
        heads.append(("BENEFICIARIES","who consumes each service",xBE))
    for name,sub,(x0,x1) in heads:
        txt(x0+6,58,name,15,INK,"start","bold",halo=False); txt(x0+6,77,sub,11.5,MUT,"start",halo=False,italic=True)
        add(f'<line x1="{x0}" y1="90" x2="{x0}" y2="1030" stroke="{LINE}" stroke-width="1"/>')
    _rx = xBE[1] if cfg.show_beneficiaries else xPR[1]
    add(f'<line x1="{_rx}" y1="90" x2="{_rx}" y2="1030" stroke="{LINE}" stroke-width="1"/>')
    add(f'<line x1="110" y1="90" x2="{W-20}" y2="90" stroke="{LINE}" stroke-width="1.2"/>')

    # ===== sources =====
    fed_top=126; st_top=655
    rect(150,fed_top,bw,fed*ys,FED); rect(150,st_top,bw,state*ys,STATE)
    lbg(150,fed_top-9,f"Federal  ${fed:.2f}",14); txt(150,fed_top-9,f"Federal  ${fed:.2f}",14,FED,"start","bold",halo=False)
    lbg(150,st_top+state*ys+18,f"State  ${state:.2f}",14); txt(150,st_top+state*ys+18,f"State  ${state:.2f}",14,"#5f7f8c","start","bold",halo=False)
    # trunk geometry
    T0=cY-100*ys/2; TB=cY+100*ys/2
    # A federal-slope bite (provider tax limits) narrows the federal band halfway
    # down its descent and leaves the gap open. cfg.fed_bite is 0 on the as-is.
    fb=cfg.fed_bite
    bites=[]
    fed_lane=(T0,T0+(fed-fb)*ys)
    st_lane=(T0+fed*ys,TB)
    if fb>0:
        _fm=(150+bw+xSG[0])/2; _fmy=(fed_top+fed_lane[0])/2
        band(150+bw,_fm,fed_top,_fmy,fed*ys,fed*ys,FED,0.8)
        band(_fm,xSG[0],_fmy,fed_lane[0],fed*ys,(fed-fb)*ys,FED,0.8)
        bites.append((cfg.fed_bite_name,_fm,_fmy+fed*ys,fb))
    else:
        band(150+bw,xSG[0],fed_top,fed_lane[0],fed*ys,fed*ys,FED,0.8)
    band(150+bw,xSG[0],st_top,st_lane[0],state*ys,state*ys,STATE,0.8)
    band(xSG[0],xSG[1],fed_lane[0],fed_lane[0],(fed-fb)*ys,(fed-fb)*ys,FED,0.82)
    band(xSG[0],xSG[1],st_lane[0],st_lane[0],state*ys,state*ys,STATE,0.82)
    rect(xSG[0],fed_lane[0],bw,(fed-fb)*ys,FED); rect(xSG[0],st_lane[0],bw,state*ys,STATE)
    txt(xSG[0]+30,fed_lane[0]+(fed-fb)*ys/2+4,f"Federal {fed:.1f}%",13,"#ffffff","start","bold",halo=False)
    txt(xSG[0]+30,st_lane[0]+state*ys/2+4,f"State {state:.1f}%",13,"#33474f","start","bold",halo=False)
    # SA combined trunk, sequential peels
    # The trunk steps once per outflow, at that outflow's own x, in ledger order.
    # Ordinary leakage steps the TOP edge down; HR-1 steps the BOTTOM edge up
    # (S-056). cfg.steps is [(name, "top"|"bot", value, x)], sorted by x.
    _T=100-fb
    rect(xSA[0],T0,bw,_T*ys,DOLLAR)
    ax=mx=None; top2=top3=T0
    _top=T0; _thk=_T; _x=xSA[0]+bw
    for _nm,_side,_v,_sx in sorted(cfg.steps,key=lambda r:r[3]):
        band(_x,_sx,_top,_top,_thk*ys,_thk*ys,DOLLAR,0.82)
        if _side=="top":
            if _nm=="admin": ax=_sx; top2=_top+_v*ys
            else: mx=_sx; top3=_top+_v*ys
            _top+=_v*ys
        else:
            bites.append((_nm,_sx,_top+_thk*ys,_v))
        _thk-=_v; _x=_sx
    band(_x,xSA[1],_top,_top,_thk*ys,_thk*ys,DOLLAR,0.82)
    top3=_top
    fexit(ax,T0,admin*ys,xSA[1]-6,250,ADMIN,f"Administration  ${admin:.2f}","state / program overhead")
    # Medicare premiums peels flush off the TOP edge like any ordinary outflow, then
    # returns to the federal lane. The return is the one sanctioned exception to the
    # downstream rule (S-055), because the money genuinely goes back (S-062).
    _mh=medicare*ys; _mk=mx+64; _mky=top2-48
    band(mx,_mk,top2,_mky,_mh,_mh,MEDI,0.72)
    add(f'<path d="M{_mk:.1f},{_mky+_mh/2:.1f} C{_mk-200:.1f},{_mky+_mh/2-80:.1f} 470,130 236,136" fill="none" stroke="{MEDI}" stroke-width="{_mh:.1f}" stroke-opacity="0.72" stroke-linecap="round"/>')
    add(f'<path d="M226,136 l16,-6 l0,12 Z" fill="{MEDI}"/>')
    lbg(252,112,f"Medicare premiums  ${medicare:.2f}",12,"start"); txt(252,112,f"Medicare premiums  ${medicare:.2f}",12,"#5f6166","start","bold",halo=False)
    lbg(252,127,"returns to the federal government (Medicaid \u2192 Medicare)",10,"start"); txt(252,127,"returns to the federal government (Medicaid \u2192 Medicare)",10,MUT,"start",halo=False,italic=True)
    rect(xSA[1],top3,bw,(mco+dual+ffs)*ys,DOLLAR)
    txt((xSA[0]+xSA[1])/2+6,cY-4,cfg.centre[0],15,"#ffffff","middle","bold",halo=False)
    txt((xSA[0]+xSA[1])/2+6,cY+16,cfg.centre[1],15,"#ffffff","middle","bold",halo=False)

    # ===== Disbursements =====
    mco_y=top3; dual_y=mco_y+mco*ys; ffs_y=dual_y+dual*ys
    peelx=1150
    band(xSA[1]+bw,peelx,mco_y,mco_y,mco*ys,mco*ys,MCO,0.82)
    band(xSA[1]+bw,peelx,dual_y,dual_y,dual*ys,dual*ys,DUAL,0.82)
    band(xSA[1]+bw,xCL[0],ffs_y,ffs_y,ffs*ys,ffs*ys,FFS,0.82)
    rect(xDI[0],mco_y,bw,mco*ys,MCO); rect(xDI[0],dual_y,bw,dual*ys,DUAL); rect(xDI[0],ffs_y,bw,ffs*ys,FFS)
    lbg(xDI[0]+24,mco_y+mco*ys/2+5,f"MCO capitation  ${mco:.2f}",13); txt(xDI[0]+24,mco_y+mco*ys/2+5,f"MCO capitation  ${mco:.2f}",13,"#1f5b57","start","bold",halo=False)
    lbg(xDI[0]+24,dual_y+dual*ys/2+5,f"Dual MCO capitation  ${dual:.2f}",13); txt(xDI[0]+24,dual_y+dual*ys/2+5,f"Dual MCO capitation  ${dual:.2f}",13,"#5a3d63","start","bold",halo=False)
    lbg(xDI[0]+24,ffs_y+ffs*ys/2+5,f"Fee-for-service  ${ffs:.2f}",13); txt(xDI[0]+24,ffs_y+ffs*ys/2+5,f"Fee-for-service  ${ffs:.2f}",13,"#36505f","start","bold",halo=False)

    # ===== Payer: peel administration, fork into earnings + MCO admin + dual-MCO admin =====
    mco_care_y=mco_y+mco_ret*ys; dual_care_y=dual_y+dual_ret*ys
    band(peelx,xCL[0],mco_care_y,mco_care_y,mco_care*ys,mco_care*ys,MCO,0.82)
    band(peelx,xCL[0],dual_care_y,dual_care_y,dual_care*ys,dual_care*ys,DUAL,0.82)
    plx=1235; planY=250
    band(peelx,plx,mco_y,planY,mco_ret*ys,mco_ret*ys,RETAIN,0.88)
    band(peelx,plx,dual_y,planY+mco_ret*ys,dual_ret*ys,dual_ret*ys,RETAIN,0.88)
    yk=planY
    if earnings > 0:
        band(plx,xPA[1]-6,yk,136,earnings*ys,earnings*ys,EARN,0.9); yk+=earnings*ys
        rect(xPA[1]-6,136,5,max(earnings*ys,4),EARN)
        lbg(xPA[1]-15,132,f"Public-company earnings  ${earnings:.2f}",13,"end"); txt(xPA[1]-15,132,f"Public-company earnings  ${earnings:.2f}",13,EARN,"end","bold",halo=False)
    if earnings > 0:
        lbg(xPA[1]-15,148,"subset of margin (est.)",10.5,"end"); txt(xPA[1]-15,148,"subset of margin (est.)",10.5,MUT,"end",halo=False,italic=True)
    band(plx,xPA[1]-6,yk,198,mco_adm*ys,mco_adm*ys,RETAIN,0.9); yk+=mco_adm*ys
    rect(xPA[1]-6,198,5,mco_adm*ys,RETAIN)
    lbg(xPA[1]-15,194,f"MCO plan administration  ${mco_adm:.2f}",13,"end"); txt(xPA[1]-15,194,f"MCO plan administration  ${mco_adm:.2f}",13,RETAIN,"end","bold",halo=False)
    lbg(xPA[1]-15,210,"non-dual MCO administration",10.5,"end"); txt(xPA[1]-15,210,"non-dual MCO administration",10.5,MUT,"end",halo=False,italic=True)
    band(plx,xPA[1]-6,yk,262,dual_adm*ys,dual_adm*ys,DUALADM,0.92); yk+=dual_adm*ys
    rect(xPA[1]-6,262,5,max(dual_adm*ys,4),DUALADM)
    lbg(xPA[1]-15,258,f"Dual MCO plan administration  ${dual_adm:.2f}",13,"end"); txt(xPA[1]-15,258,f"Dual MCO plan administration  ${dual_adm:.2f}",13,DUALADM,"end","bold",halo=False)
    lbg(xPA[1]-15,274,"dual-plan administration",10.5,"end"); txt(xPA[1]-15,274,"dual-plan administration",10.5,MUT,"end",halo=False,italic=True)

    # ===== CLAIMS: 3 care lanes fan into 6 provider bars =====
    gg=50; htot=sum(node[p] for p in order)*ys+(len(order)-1)*gg; ntop=cY-htot/2
    node_y={}; y=ntop
    for p in order: node_y[p]=y; y+=node[p]*ys+gg
    barL=xPR[0]; barW=140; barR=barL+barW
    lane_src={"MCO":mco_care_y,"Dual":dual_care_y,"FFS":ffs_y}
    comp={"MCO":mcoc_n,"Dual":dualc_n,"FFS":ffs_n}; lc={"MCO":MCO,"Dual":DUAL,"FFS":FFS}
    ncur={p:node_y[p] for p in order}
    if fraud > 0:
        fh=max(fraud*ys,3.0)
        # Documented fraud runs clear beneath the provider bars and stops ON the
        # providers / beneficiaries boundary. Providers receive it, so it must not cross
        # into the beneficiary column, and it must not tangle with the Rx drugs bar.
        _fy=max(node_y[order[-1]]+node[order[-1]]*ys, ffs_y+ffs*ys)+40
        add(f'<path d="M{xCL[0]+6:.1f},{ffs_y+ffs*ys-fh/2:.1f} C{xCL[0]+70:.1f},{ffs_y+ffs*ys+70:.1f} {xPR[0]-120:.1f},{_fy:.1f} {xPR[1]-8:.1f},{_fy:.1f}" fill="none" stroke="{FRAUD}" stroke-width="{fh:.1f}" stroke-opacity="0.95" stroke-linecap="round"/>')
        rect(xPR[1]-8,_fy-max(fh,5)/2,6,max(fh,5),FRAUD)
        lbg(xPR[1]-14,_fy-8,f"Documented fraud  ${fraud:.2f}",12,"end"); txt(xPR[1]-14,_fy-8,f"Documented fraud  ${fraud:.2f}",12,FRAUD,"end","bold",halo=False)
        lbg(xPR[1]-14,_fy+9,"providers receive it; it is not services delivered (not to scale)",9.5,"end"); txt(xPR[1]-14,_fy+9,"providers receive it; it is not services delivered (not to scale)",9.5,MUT,"end",halo=False,italic=True)
    for p in order:
        for L in ["MCO","Dual","FFS"]:
            v=comp[L][p]; h=v*ys
            if v<=0: continue
            band(xCL[0],barL,lane_src[L],ncur[p],h,h,lc[L],0.62 if L!="FFS" else 0.8, dash=(L!="FFS"))
            lane_src[L]+=h; ncur[p]+=h
        # ===== PROVIDERS =====
    for p in order:
        yy=node_y[p]
        for L,val in [("MCO",mcoc_n[p]),("Dual",dualc_n[p]),("FFS",ffs_n[p])]:
            rect(barL,yy,barW,val*ys,lc[L]); yy+=val*ys
        nm=disp.get(p,p)+("*" if p=="Other" else "")
        lbg(barL+barW/2,node_y[p]-9,f"{nm}  ${node[p]:.2f}",13.5,"middle"); txt(barL+barW/2,node_y[p]-9,f"{nm}  ${node[p]:.2f}",13.5,INK,"middle","bold",halo=False)
    if cfg.show_beneficiaries:
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

    # Declared absences sit where the missing detail would have been, so the
    # reader sees what is not here rather than inferring it (S-071).
    if cfg.absent:
        _ax = xBE[0]+20 if not cfg.show_beneficiaries else xBE[0]+20
        txt(_ax,140,"NOT SHOWN, and not estimated:",13,"#8B5A5A","start","bold",halo=False)
        for _i,_a in enumerate(cfg.absent):
            txt(_ax,166+_i*22,"\u2022  "+_a,12,MUT,"start",halo=False)
        txt(_ax,166+len(cfg.absent)*22+14,
            "Absent data is left absent. Filling a state gap with a national share",
            11,MUT,"start",halo=False,italic=True)
        txt(_ax,166+len(cfg.absent)*22+30,
            "would produce a modelled figure wearing a measured figure's clothes.",
            11,MUT,"start",halo=False,italic=True)

    # ===== BOTTOM TRACKER: running balance of the $100 (fonts 2x) =====
    add(f'<line x1="110" y1="1030" x2="{W-20}" y2="1030" stroke="{LINE}" stroke-width="1.2"/>')
    by=1100
    # Checkpoints: shared furniture, identical on every artifact (S-060). $100 sits
    # under the FEDERAL column, before federal and state combine. Health services
    # delivered sits on the providers / beneficiaries boundary.
    # The claims-fan bite (directed payment caps) can only be placed once the
    # fee-for-service lane geometry exists, so it joins the bite list here.
    if cfg.claims_hr1>0:
        bites.append((cfg.claims_hr1_name,xCL[0]+2,ffs_y+ffs*ys,cfg.claims_hr1))
    cps=[(205,"$100.00",cfg.cp0_label),
         (820,f"${100-fb-admin-medicare-cfg.sa_hr1:.2f}",["Disbursed"]),
         (1300,f"${mco_care+dual_care+ffs:.2f}",["Claims paid"]),
         (1760,f"${mco_care+dual_care+ffs-fraud-cfg.claims_hr1:.2f}",["Health Services","delivered"])]
    ordinaries=[(xSA[1]-8,admin+medicare,"administration + Medicare premiums"),
                (xPA[1]-8,mco_ret+dual_ret,"plan administration + earnings"),
                (xCL[1]-8,fraud,"documented fraud")]
    ordinaries=[r for r in ordinaries if r[1] > 0.004]
    hr1s=cfg.tracker_hr1
    TRKINK="#111418"; TRKGREY="#8e9298"; TRKWARM="#8B5A5A"
    add(f'<line x1="{cps[0][0]}" y1="{by}" x2="{cps[-1][0]}" y2="{by}" stroke="{TRKINK}" stroke-width="3.4" stroke-opacity="0.85"/>')
    for x,val,lab in cps:
        add(f'<circle cx="{x}" cy="{by}" r="11" fill="{TRKINK}"/>')
        txt(x,by-24,val,36,TRKINK,"middle","bold",halo=False)
        for j,ln in enumerate(lab):
            txt(x,by+80+j*30,ln,25,TRKINK,"middle","bold",halo=False)
    for x,v,lab in ordinaries:
        if v<=0.004: continue
        txt(x,by-58,f"\u2212${v:.2f}",24,TRKGREY,"end","bold",halo=False)
        txt(x,by-40,lab,12,MUT,"end",halo=False,italic=True)
    for x,v,lab in hr1s:
        if v<=0.004: continue
        txt(x,by+28,f"\u2212${v:.2f}",24,TRKWARM,"end","bold",halo=False)
        txt(x,by+46,lab,12,TRKWARM,"end",halo=False,italic=True)

    return svg, _draw_hr1(cfg, bites, ys, TB)


def _solve_pies(order, node, gt):
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
    return {p:[M[p][g]/sum(M[p].values()) for g in G] for p in order}

# --------------------------------------------------------------------------
def _draw_hr1(cfg, bites, ys, TB):
    """HR-1 tributaries. Each leaves flush with the edge it comes from and
    terminates downstream of its own bite x (S-055, S-057). Terminal geometry
    comes from cfg.hr1_term, sourced from outflows.py, never written twice."""
    global svg
    if not bites:
        return []
    WARM="#8B5A5A"; WARMD="#6f4747"
    _saved, svg = svg, []
    add('<defs><pattern id="hr1hatch" width="6" height="6" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" '
        'stroke="#6f4747" stroke-width="2.1" stroke-opacity="0.55"/></pattern></defs>')
    add(f'<line x1="330" y1="788" x2="1560" y2="788" stroke="{WARM}" stroke-width="1.1" '
        f'stroke-dasharray="7 5" stroke-opacity="0.7"/>')
    txt(336,780,"HR-1 TAKES THESE OUT",11,WARM,"start","bold",halo=False)
    for name,xb,yb,v in bites:
        xt,row,sub = cfg.hr1_term[name]
        assert xt > xb, f"{name}: terminal {xt} is upstream of its bite {xb} (S-057)"
        th=max(v*ys,3.4); yt=(806 if row<0 else 800+row*62)
        y0=yb-v*ys                      # flush with the edge (S-057)
        band(xb,xt,y0,yt,th,th,WARM,0.74)
        xm=(xb+xt)/2
        add(f'<path d="M{xb:.1f},{y0:.1f} C{xm:.1f},{y0:.1f} {xm:.1f},{yt:.1f} {xt:.1f},{yt:.1f} '
            f'L{xt:.1f},{yt+th:.1f} C{xm:.1f},{yt+th:.1f} {xm:.1f},{y0+th:.1f} {xb:.1f},{y0+th:.1f} Z" '
            f'fill="url(#hr1hatch)"/>')
        rect(xt,yt,6,max(th,4),WARMD)
        an="end" if row<0 else "start"; lx=xt-8 if row<0 else xt
        ly=yt+max(th,4)+15
        lbg(lx,ly,name,12,an);   txt(lx,ly,name,12,WARMD,an,"bold",halo=False)
        lbg(lx,ly+14,sub,10,an); txt(lx,ly+14,sub,10,MUT,an,halo=False,italic=True)
        lbg(lx,ly+28,f"\u2212${v:.2f}",12,an)
        txt(lx,ly+28,f"\u2212${v:.2f}",12,WARM,an,"bold",halo=False)
    out, svg = svg, _saved
    return out
