import math
import tracker as TR
import outflows as OF
FAN_STACK_TOP=806.0
from outflows import (OUTFLOWS, fan_rows, fan_crossings, resolve_bite_order,
                      label_of as OUTFLOWS_label)
# ===== Medicaid Dollar-Flow Sankey, DRAFT V.4 (Public Comment) =====
# H was 1240, which left the short-name row 4 units from the canvas edge and no
# room for a second line. A bite whose short name cannot fit between its
# neighbouring dots wraps (tracker.wrap_short, STYLE_GUIDE 4.8), so the canvas
# carries the extra line. W is untouched: column register is frozen (1.2), panel
# HEIGHT never was.
W,H=2200,1376; cY=540; ys=4.4; bw=18
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
    oversight, fo = cfg.oversight, cfg.fed_outside
    fed, state, admin, medicare, mco, dual, ffs, mco_ret, dual_ret, earnings, adm_marg, mco_adm, dual_adm, mco_care, dual_care, node, fraud, ffs_n, mcoc_n, dualc_n, gt = (
        cfg.fed, cfg.state, cfg.admin, cfg.medicare, cfg.mco, cfg.dual, cfg.ffs, cfg.mco_ret, cfg.dual_ret, cfg.earnings, cfg.adm_marg, cfg.mco_adm, cfg.dual_adm, cfg.mco_care, cfg.dual_care, cfg.node, cfg.fraud, cfg.ffs_n, cfg.mcoc_n, cfg.dualc_n, cfg.gt)
    order = cfg.order
    disp = cfg.disp
    # ABSENT DATA IS ABSENT (S-071). A missing lane or column is omitted and
    # declared, never estimated from a national share (S-068).
    pie_frac = _solve_pies(order, node, gt) if cfg.show_beneficiaries else None
    add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>')
    # phase headers + dividers
    # Column sub-labels name the FUNCTION the column performs, not a note about
    # how the drawing was put together (JW, 2026-09-04).
    heads=[("FEDERAL","federal appropriation",xFED),("STATE GOVERNMENT","blended cost allocation",xSG),
     ("STATE AGENCY","budgeted to Medicaid",xSA),("DISBURSEMENTS","payment mechanisms",xDI),
     ("PAYER","MCO administration",xPA),("CLAIMS","claims paid to providers",xCL),("PROVIDERS","sized by spend",xPR)]
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
    # The trunk is what arrives at the state agency: everything that entered,
    # less anything that peeled before the hundred was struck. D-70. This used
    # to read the literal 100, which asserted that the sources sum to 100.
    _ENTER=fed+state; _ARRIVE=_ENTER-fo
    T0=cY-_ARRIVE*ys/2; TB=cY+_ARRIVE*ys/2
    # A federal-slope bite (provider tax limits) narrows the federal band halfway
    # down its descent and leaves the gap open. cfg.fed_bite is 0 on the as-is.
    fb=cfg.fed_bite
    bites=[]
    fed_lane=(T0,T0+(fed-fb-fo)*ys)
    st_lane=(T0+(fed-fo)*ys,TB)
    if fb+fo>0:
        _fm=(150+bw+xSG[0])/2; _fmy=(fed_top+fed_lane[0])/2
        # The vaccine money comes off the TOP edge at the earliest point there
        # is — the moment the appropriation leaves its own bar — so the band
        # that crosses the page is already the blended dollar. D-71.
        band(150+bw,_fm,fed_top+fo*ys,_fmy,(fed-fo)*ys,(fed-fo)*ys,FED,0.8)
        band(_fm,xSG[0],_fmy,fed_lane[0],(fed-fo)*ys,(fed-fb-fo)*ys,FED,0.8)
        if fb>0:
            bites.append((cfg.fed_bite_name,_fm,_fmy+fed*ys,fb))
        if fo>0:
            # Not a bite. Money doing its job elsewhere, so it gets a plain grey
            # label on the federal slope and no terminal below the rule. D-71.
            # Drawn like the Medicare premiums return, not like an HR-1 bite:
            # a grey band that leaves the federal slope, turns back and
            # terminates with an arrowhead. The money is not lost, it is doing
            # its job somewhere this diagram does not go. D-71.
            # Out along the top, one fold, back to a terminal. One doubling
            # back and no swirl: two reversals would suggest the money went
            # somewhere and came back, and it does not.
            _vh=max(fo*ys,2.4); _vk=150+bw+96; _vt=fed_top-26
            band(150+bw,_vk,fed_top,fed_top-12,fo*ys,fo*ys,MEDI,0.72)
            _vm=fed_top-12+fo*ys/2
            add(f'<path d="M{_vk:.1f},{_vm:.1f} C{_vk+86:.1f},{_vm:.1f} '
                f'{_vk+86:.1f},{_vt:.1f} 246,{_vt:.1f}" fill="none" '
                f'stroke="{MEDI}" stroke-width="{_vh:.1f}" stroke-opacity="0.72" '
                f'stroke-linecap="round"/>')
            add(f'<path d="M236,{_vt:.1f} l16,-6 l0,12 Z" fill="{MEDI}"/>')
            # The label cannot sit to the RIGHT of the arrowhead the way the
            # Medicare one does: at this height the state government band is
            # already there. It goes left, into the white column, on two short
            # lines. The rest of the story is EN-49.
            # One line, not two: the Medicare label sits 26 units below and a
            # second line would close the gap to nothing.
            _ol=f"{cfg.fed_outside_name}  ${fo:.2f}   never blended, terminates at CDC"
            lbg(252,_vt-3,_ol,10.5,"start")
            txt(252,_vt-3,_ol,10.5,"#5f6166","start","bold",halo=False)
    else:
        band(150+bw,xSG[0],fed_top,fed_lane[0],fed*ys,fed*ys,FED,0.8)  # no bite
    band(150+bw,xSG[0],st_top,st_lane[0],state*ys,state*ys,STATE,0.8)
    band(xSG[0],xSG[1],fed_lane[0],fed_lane[0],(fed-fb-fo)*ys,(fed-fb-fo)*ys,FED,0.82)
    band(xSG[0],xSG[1],st_lane[0],st_lane[0],state*ys,state*ys,STATE,0.82)
    rect(xSG[0],fed_lane[0],bw,(fed-fb-fo)*ys,FED); rect(xSG[0],st_lane[0],bw,state*ys,STATE)
    # The blended share, not the appropriation share. They differ once anything
    # 100 percent federal peels before the blend, and that difference is the
    # finding D-70 exposes.
    _blend=(fed-fo)/_ARRIVE*100 if _ARRIVE else 0.0
    txt(xSG[0]+30,fed_lane[0]+(fed-fb-fo)*ys/2+4,f"Federal {_blend:.1f}%",13,"#ffffff","start","bold",halo=False)
    txt(xSG[0]+30,st_lane[0]+state*ys/2+4,f"State {state/_ARRIVE*100 if _ARRIVE else 0:.1f}%",13,"#33474f","start","bold",halo=False)
    # SA combined trunk, sequential peels
    # The trunk steps once per outflow, at that outflow's own x, in ledger order.
    # Ordinary leakage steps the TOP edge down; HR-1 steps the BOTTOM edge up
    # (S-056). cfg.steps is [(name, "top"|"bot", value, x)], sorted by x.
    _T=_ARRIVE-fb
    rect(xSA[0],T0,bw,_T*ys,DOLLAR)
    ax=mx=ox=None; top3=T0; origin={}
    _top=T0; _thk=_T; _x=xSA[0]+bw
    # Bite order for the ordinary peels is SOLVED, not declared: whichever
    # terminates higher peels first, so the two never swap places (STYLE_GUIDE 2.9).
    for _nm,_side,_v,_sx in sorted(resolve_bite_order(cfg.steps),key=lambda r:r[3]):
        band(_x,_sx,_top,_top,_thk*ys,_thk*ys,DOLLAR,0.82)
        if _side=="top":
            # Each peel records its OWN origin. Reading one outflow's origin off
            # another's step is what made the order un-swappable before.
            origin[_nm]=_top
            if _nm=="admin": ax=_sx
            elif _nm=="oversight": ox=_sx
            else: mx=_sx
            _top+=_v*ys
        else:
            bites.append((_nm,_sx,_top+_thk*ys,_v))
        _thk-=_v; _x=_sx
    band(_x,xSA[1],_top,_top,_thk*ys,_thk*ys,DOLLAR,0.82)
    top3=_top
    fexit(ax,origin["admin"],admin*ys,xSA[1]-6,250,ADMIN,f"Administration  ${admin:.2f}","state / program overhead")
    # D-72 split the old $5.07 three ways, but only two of the three were ever
    # drawn: the trunk narrowed by this $0.10 with nothing on the page to say
    # where it went. A peel that steps the trunk and draws no exit is money
    # leaving the diagram unexplained.
    if ox is not None and oversight > 0.004:
        fexit(ox,origin["oversight"],oversight*ys,xSA[1]-6,206,ADMIN,
              f"Federal oversight  ${oversight:.2f}",
              "fraud control units, survey and certification")
    # Medicare premiums peels flush off the TOP edge like any ordinary outflow, then
    # returns to the federal lane. The return is the one sanctioned exception to the
    # downstream rule (S-055), because the money genuinely goes back (S-062).
    _mh=medicare*ys; _mk=mx+64; _mky=origin["medicare"]-48
    band(mx,_mk,origin["medicare"],_mky,_mh,_mh,MEDI,0.72)
    # The return used to terminate at y=136, hard against the top of the plot,
    # for no reason except that nothing had ever been drawn above it. The
    # federal band's top edge at this x is y=223, so there are 87 units of
    # clear space underneath. It sits in that space now, which leaves the top
    # line for the vaccine peel. Nothing about the arithmetic changes.
    _my=205
    add(f'<path d="M{_mk:.1f},{_mky+_mh/2:.1f} C{_mk-200:.1f},{_mky+_mh/2-80:.1f} 470,{_my-6} 236,{_my}" fill="none" stroke="{MEDI}" stroke-width="{_mh:.1f}" stroke-opacity="0.72" stroke-linecap="round"/>')
    add(f'<path d="M226,{_my} l16,-6 l0,12 Z" fill="{MEDI}"/>')
    lbg(252,_my-24,f"Medicare premiums  ${medicare:.2f}",12,"start"); txt(252,_my-24,f"Medicare premiums  ${medicare:.2f}",12,"#5f6166","start","bold",halo=False)
    lbg(252,_my-9,"returns to the federal government (Medicaid \u2192 Medicare)",10,"start"); txt(252,_my-9,"returns to the federal government (Medicaid \u2192 Medicare)",10,MUT,"start",halo=False,italic=True)
    rect(xSA[1],top3,bw,(mco+dual+ffs)*ys,DOLLAR)
    txt((xSA[0]+xSA[1])/2+6,cY-4,cfg.centre[0],15,"#ffffff","middle","bold",halo=False)
    txt((xSA[0]+xSA[1])/2+6,cY+16,cfg.centre[1],15,"#ffffff","middle","bold",halo=False)

    # ===== Disbursements =====
    # A collapsed lane is drawn as nothing at all. Its width is already zero,
    # so the stacking below is unaffected; what has to go is the label, the
    # node bar and the peel, because a $0.00 label is a claim that the lane
    # exists and is empty, which is a different statement from absent.
    _off=set(getattr(cfg,'collapsed',()))
    on=lambda k: k not in _off
    mco_y=top3; dual_y=mco_y+mco*ys; ffs_y=dual_y+dual*ys
    peelx=1150
    if on('mco'):  band(xSA[1]+bw,peelx,mco_y,mco_y,mco*ys,mco*ys,MCO,0.82)
    if on('dual'): band(xSA[1]+bw,peelx,dual_y,dual_y,dual*ys,dual*ys,DUAL,0.82)
    if on('ffs'):  band(xSA[1]+bw,xCL[0],ffs_y,ffs_y,ffs*ys,ffs*ys,FFS,0.82)
    if on('mco'):  rect(xDI[0],mco_y,bw,mco*ys,MCO)
    if on('dual'): rect(xDI[0],dual_y,bw,dual*ys,DUAL)
    if on('ffs'):  rect(xDI[0],ffs_y,bw,ffs*ys,FFS)
    if on('mco'): lbg(xDI[0]+24,mco_y+mco*ys/2+5,f"MCO capitation  ${mco:.2f}",13); txt(xDI[0]+24,mco_y+mco*ys/2+5,f"MCO capitation  ${mco:.2f}",13,"#1f5b57","start","bold",halo=False)
    if on('dual'): lbg(xDI[0]+24,dual_y+dual*ys/2+5,f"Dual MCO capitation  ${dual:.2f}",13); txt(xDI[0]+24,dual_y+dual*ys/2+5,f"Dual MCO capitation  ${dual:.2f}",13,"#5a3d63","start","bold",halo=False)
    if on('ffs'): lbg(xDI[0]+24,ffs_y+ffs*ys/2+5,f"Fee-for-service  ${ffs:.2f}",13); txt(xDI[0]+24,ffs_y+ffs*ys/2+5,f"Fee-for-service  ${ffs:.2f}",13,"#36505f","start","bold",halo=False)

    # ===== Payer: peel administration, fork into earnings + MCO admin + dual-MCO admin =====
    mco_care_y=mco_y+mco_ret*ys; dual_care_y=dual_y+dual_ret*ys
    if on('mco'):  band(peelx,xCL[0],mco_care_y,mco_care_y,mco_care*ys,mco_care*ys,MCO,0.82)
    if on('dual'): band(peelx,xCL[0],dual_care_y,dual_care_y,dual_care*ys,dual_care*ys,DUAL,0.82)
    plx=1235; planY=250
    if on('mco'):  band(peelx,plx,mco_y,planY,mco_ret*ys,mco_ret*ys,RETAIN,0.88)
    if on('dual'): band(peelx,plx,dual_y,planY+mco_ret*ys,dual_ret*ys,dual_ret*ys,RETAIN,0.88)
    yk=planY
    if earnings > 0:
        band(plx,xPA[1]-6,yk,136,earnings*ys,earnings*ys,EARN,0.9); yk+=earnings*ys
        rect(xPA[1]-6,136,5,max(earnings*ys,4),EARN)
        lbg(xPA[1]-15,132,f"Public-company earnings  ${earnings:.2f}",13,"end"); txt(xPA[1]-15,132,f"Public-company earnings  ${earnings:.2f}",13,EARN,"end","bold",halo=False)
    if earnings > 0:
        lbg(xPA[1]-15,148,"subset of margin (est.)",10.5,"end"); txt(xPA[1]-15,148,"subset of margin (est.)",10.5,MUT,"end",halo=False,italic=True)
    if on('mco'):
     band(plx,xPA[1]-6,yk,198,mco_adm*ys,mco_adm*ys,RETAIN,0.9); yk+=mco_adm*ys
     rect(xPA[1]-6,198,5,mco_adm*ys,RETAIN)
     lbg(xPA[1]-15,194,f"MCO plan administration  ${mco_adm:.2f}",13,"end"); txt(xPA[1]-15,194,f"MCO plan administration  ${mco_adm:.2f}",13,RETAIN,"end","bold",halo=False)
     lbg(xPA[1]-15,210,"non-dual MCO administration",10.5,"end"); txt(xPA[1]-15,210,"non-dual MCO administration",10.5,MUT,"end",halo=False,italic=True)
    if on('dual'):
     band(plx,xPA[1]-6,yk,262,dual_adm*ys,dual_adm*ys,DUALADM,0.92); yk+=dual_adm*ys
     rect(xPA[1]-6,262,5,max(dual_adm*ys,4),DUALADM)
     lbg(xPA[1]-15,258,f"Dual MCO plan administration  ${dual_adm:.2f}",13,"end"); txt(xPA[1]-15,258,f"Dual MCO plan administration  ${dual_adm:.2f}",13,DUALADM,"end","bold",halo=False)
     lbg(xPA[1]-15,274,"dual-plan administration",10.5,"end"); txt(xPA[1]-15,274,"dual-plan administration",10.5,MUT,"end",halo=False,italic=True)

    # ===== CLAIMS: 3 care lanes fan into 6 provider bars =====
    gg=50; htot=sum(node[p] for p in order)*ys+(len(order)-1)*gg; ntop=cY-htot/2
    node_y={}; y=ntop
    for p in order: node_y[p]=y; y+=node[p]*ys+gg
    barL=xPR[0]; barW=140; barR=barL+barW
    _LK={"MCO":"mco","Dual":"dual","FFS":"ffs"}
    LANES=[L for L in ("MCO","Dual","FFS") if on(_LK[L])]
    lane_src={"MCO":mco_care_y,"Dual":dual_care_y,"FFS":ffs_y}
    comp={"MCO":mcoc_n,"Dual":dualc_n,"FFS":ffs_n}; lc={"MCO":MCO,"Dual":DUAL,"FFS":FFS}
    ncur={p:node_y[p] for p in order}
    if fraud > 0:
        fh=max(fraud*ys,3.0)
        # Documented fraud is drawn as a RIBBON in the same family as the lanes
        # above it, not as a swooping stroke across the canvas (JW, 2026-09-04).
        # It leaves the claims column where the other lanes do and lands at the
        # RIGHT END OF THE PROVIDER BARS, because providers are where fraud
        # happens in this ledger. It used to stop on the providers / beneficiaries
        # boundary, which read as though beneficiaries were party to it.
        #
        # It also stays ABOVE the HR-1 rule. Fraud is not something HR-1 takes
        # out, and a line that dives through that zone says it is.
        _fy = max(node_y[order[-1]] + node[order[-1]] * ys,
                  ffs_y + ffs * ys) + 34
        _fx0, _fx1 = xCL[0] + 6, barR
        _fm = (_fx0 + _fx1) / 2
        _fsy = ffs_y + ffs * ys - fh / 2
        add(f'<path d="M{_fx0:.1f},{_fsy:.1f} C{_fm:.1f},{_fsy:.1f} '
            f'{_fm:.1f},{_fy:.1f} {_fx1:.1f},{_fy:.1f}" fill="none" '
            f'stroke="{FRAUD}" stroke-width="{fh:.1f}" stroke-opacity="0.95" '
            f'stroke-linecap="round"/>')
        rect(barR, _fy - max(fh, 5) / 2, 6, max(fh, 5), FRAUD)
        lbg(barR - 6, _fy - 9, f"Documented fraud  ${fraud:.2f}", 12, "end")
        txt(barR - 6, _fy - 9, f"Documented fraud  ${fraud:.2f}", 12, FRAUD, "end", "bold", halo=False)
        lbg(barR - 6, _fy + 8, "providers receive it; it is not services delivered (not to scale)", 9.5, "end")
        txt(barR - 6, _fy + 8, "providers receive it; it is not services delivered (not to scale)", 9.5, MUT, "end", halo=False, italic=True)
    for p in order:
        for L in ["MCO","Dual","FFS"]:
            v=comp[L][p]; h=v*ys
            if v<=0: continue
            band(xCL[0],barL,lane_src[L],ncur[p],h,h,lc[L],0.62 if L!="FFS" else 0.8, dash=(L!="FFS"))
            lane_src[L]+=h; ncur[p]+=h
        # ===== PROVIDERS =====
    for p in order:
        yy=node_y[p]
        for L,val in [(L,comp[L][p]) for L in LANES]:
            rect(barL,yy,barW,val*ys,lc[L]); yy+=val*ys
        nm=disp.get(p,p)+("*" if p=="Other" else "")
        lbg(barL+barW/2,node_y[p]-9,f"{nm}  ${node[p]:.2f}",13.5,"middle"); txt(barL+barW/2,node_y[p]-9,f"{nm}  ${node[p]:.2f}",13.5,INK,"middle","bold",halo=False)
    _ben_floor = {}
    _key_at = None
    if cfg.show_beneficiaries:
        # ===== BENEFICIARIES: two staggered columns; each pie aligned to its bar's centre =====
        xLcol=1885; xRcol=2090
        OVERLAY_PX = 34.0      # px per $, overlay bars only. See EN-46.
        _ov_bottom = {}; _pie_geom = {}
        for i,p in enumerate(order):
            cx=xLcol if i%2==0 else xRcol
            cy=node_y[p]+node[p]*ys/2; r=16.8*math.sqrt(node[p]); a0=rot_for(pie_frac[p])
            if p=="Rx drugs": a0+=30   # nudge so the small outside labels clear the $ below
            _prior = cfg.prior_node.get(p)
            pie(cx,cy,r,pie_frac[p],[CHILD,ADULT,DIS,AGED],a0)
            pielabels(cx,cy,r,pie_frac[p],a0)
            nm=disp.get(p,p)+("*" if p=="Other" else "")
            lbg(cx,cy-r-10,nm,19.5,"middle"); txt(cx,cy-r-10,nm,19.5,INK,"middle","bold",halo=False)
            lbg(cx,cy+r+22,f"${node[p]:.2f}",19.5,"middle"); txt(cx,cy+r+22,f"${node[p]:.2f}",19.5,INK,"middle","bold",halo=False)
            # ---- BENEFICIARY OVERLAY (JW, this session) ----------------------
            # Dollars and cents out of each service, on ONE scale across all six
            # so the bars are comparable with each other by eye. Percentages are
            # deliberately not used: the pies already carry percentages, on a
            # different base, and two differently-based percentages on the same
            # mark is how a reader comes to read one as the other.
            #
            # OVERLAY_PX is the overlay's own scale and is NOT the flow's: the
            # decrements are an order of magnitude smaller than the nodes and
            # would be invisible at the flow's px-per-dollar. It is declared here
            # and stated on the artifact, because a bar on an undeclared scale is
            # a bar that invites the wrong comparison (EN-46).
            if _prior and _prior > node[p]:
                _dv = _prior - node[p]
                _bw = _dv * OVERLAY_PX
                _d = f"\u2212${_dv:.2f}"
                _tw = len(_d) * 17 * 0.58
                # ONE row: bar then figure, not bar over figure. The pies are
                # pinned to their provider bars' centres and cannot be moved to
                # make room, so the overlay has to earn its space in height, not
                # be given it.
                _by = cy + r + 46
                _x0 = cx - (_bw + 8 + _tw) / 2
                rect(_x0, _by - 9, _bw, 10, "#8B5A5A")
                lbg(_x0+_bw+8, _by, _d, 17, "start")
                txt(_x0+_bw+8, _by, _d, 17, "#8B5A5A", "start", "bold", halo=False)
                _ov_bottom[p] = _by + 6
                _ben_floor[p] = _by + 6
                _pie_geom[p] = (i, cx, cy, r)

        # GATE. The overlay hangs below a pie that is pinned to its provider
        # bar, and the next pie in the same staggered column is pinned too, so
        # nothing here can be nudged: if the block does not fit, the fit is the
        # finding and the build says so. S-078's lesson on the tracker, applied
        # to the one other place on the canvas where furniture is pinned.
        for p, bot in _ov_bottom.items():
            i, _cx, _cy, _r = _pie_geom[p]
            if i + 2 >= len(order):
                continue
            q = order[i + 2]
            qy = node_y[q] + node[q]*ys/2
            qr = 16.8*math.sqrt(node[q])
            name_top = qy - qr - 10 - 19.5
            if bot > name_top:
                print(f"  WARNING  beneficiary overlay: {p} reaches y={bot:.0f}, "
                      f"past {q}'s name at y={name_top:.0f}")

        # beneficiary legend (compact, horizontal)
        lx=xBE[0]+20; ly=108
        txt(lx,ly,"Share of each service consumed by:",12.5,INK,"start","bold",halo=False)
        gx=lx
        for g,c in zip(G,[CHILD,ADULT,DIS,AGED]):
            rect(gx,ly+11,13,13,c); txt(gx+18,ly+21,g,12,INK,"start",halo=False)
            gx+=40+len(g)*12*0.55
        txt(lx,ly+42,"numbers = % of that node's dollars (black sits outside)",10.5,MUT,"start",halo=False,italic=True)
        # The overlay's key reads BELOW the pies, beside the bars it explains
        # (JW, 2026-09-11), not at the top of the column where it sat above the
        # thing it was describing. Its scale is declared on the artifact and not
        # only in the endnote: the bars are an order of magnitude larger per
        # dollar than the flow, and an undeclared scale invites exactly the
        # wrong comparison.
        if _ben_floor and any(v > 0 for v in cfg.prior_node.values()):
            _key_at = (lx, max(_ben_floor.values()) + 34)

    # Where the declaration goes: below the last pie and its overlay, which is
    # the only clear space in this column. Computed, not guessed.
    _abs_y = int(max(_ben_floor.values()) + 30) if _ben_floor else 140

    # ===== BOTTOM TRACKER: running balance of the $100 (fonts 2x) =====
    add(f'<line x1="110" y1="{TR.RULE_Y:.0f}" x2="{W-20}" y2="{TR.RULE_Y:.0f}" stroke="{LINE}" stroke-width="1.2"/>')
    by=1100
    # Checkpoints: shared furniture, identical on every artifact (S-060). $100 sits
    # under the FEDERAL column, before federal and state combine. Health services
    # The claims-fan bite can only be placed once the fee-for-service lane
    # geometry exists, so it joins the bite list here.
    if cfg.claims_hr1>0:
        # Directed payment caps come out of MANAGED CARE, not fee-for-service.
        # A state directed payment is defined at 42 CFR 438.6(c) as a contract
        # arrangement directing an MCO's, PIHP's or PAHP's expenditures; it has no
        # fee-for-service counterpart, because there is no plan contract to direct.
        # This carved the bite off the bottom of the FFS band, which told the
        # reader the opposite of what the instrument is. It now leaves the bottom
        # of the dual-MCO care lane, the lower edge of the managed-care block at
        # this column. The ribbon then crosses the FFS lane on its way down, which
        # is a body crossing and correct (S-076, STYLE_GUIDE 2.9c).
        # It leaves the TOP edge of the managed-care block, not the bottom. The
        # bottom edge is measured at 553.8 and the fee-for-service lane starts at
        # exactly 553.8 — no gap — so a bite taken there sits on a shared edge and
        # reads as either lane. The top edge has peeled-off white space above it
        # and is unambiguous.
        bites.append((cfg.claims_hr1_name,xCL[0]+2,mco_care_y+cfg.claims_hr1*ys,cfg.claims_hr1))
    subs = cfg.subtractions(dict(vfc=fo, adm_med=admin+oversight+medicare,
                                 plan=mco_ret+dual_ret, fraud=fraud))
    _live = [s for s in subs if s[1] > 0.004]
    # D-73. The line measures the whole run, so it starts where the diagram
    # starts — at what enters, not at the hundred. S-102.
    anchors, marks = TR.ledger(
        subs,
        {s[4]: OF.decrement_x(s[4]) for s in _live},
        {s[4]: OF.decrement_span(s[4])[0] for s in _live},
        start=fed+state)
    for a, b, g in TR.collisions(anchors, marks):
        print(f"  WARNING  anchor labels overlap: {a} / {b} by {-g:.0f} units")
    for a, b, g in TR.shape_gap(marks):
        print(f"  NOTE     markers {a} / {b} sit {g:.0f} units apart on the line")
    tiers = TR.mark_tiers(marks, anchors)

    add(f'<line x1="{anchors[0]["x"]:.0f}" y1="{TR.BY}" x2="{anchors[-1]["x"]:.0f}" '
        f'y2="{TR.BY}" stroke="{TR.INK}" stroke-width="3.4" stroke-opacity="0.85"/>')

    # Decrement markers, reading ABOVE the line. Class carries in the SHAPE as
    # well as the colour: rhombus HR-1, square administration, triangle fraud.
    # Each shows only its own amount and name — every sum is at an anchor.
    for m in marks:
        x, r, c = m["x"], TR.MARK_R, TR.COLOUR[m["cls"]]
        y = TR.BY
        t = tiers[m["short"]] * TR.MARK_TIER
        if m["cls"] == "hr1":
            add(f'<polygon points="{x:.1f},{y-r:.1f} {x+r:.1f},{y:.1f} '
                f'{x:.1f},{y+r:.1f} {x-r:.1f},{y:.1f}" fill="{c}"/>')
        elif m["cls"] == "fraud":
            add(f'<polygon points="{x:.1f},{y-r:.1f} {x+r*0.95:.1f},{y+r*0.78:.1f} '
                f'{x-r*0.95:.1f},{y+r*0.78:.1f}" fill="{c}"/>')
        else:
            h = r * 0.88
            add(f'<rect x="{x-h:.1f}" y="{y-h:.1f}" width="{h*2:.1f}" '
                f'height="{h*2:.1f}" fill="{c}"/>')
        if t:
            # A stepped-down block is led back to its own marker, or the reader
            # has to guess which shape the words belong to.
            add(f'<line x1="{x:.1f}" y1="{y+r+4:.1f}" x2="{x:.1f}" '
                f'y2="{y+t+TR.MARK_AMT_Y-14:.1f}" stroke="{c}" stroke-width="1.1" '
                f'stroke-opacity="0.55"/>')
        txt(x, y+t+TR.MARK_AMT_Y, f"\u2212${m['amount']:.2f}", TR.MARK_AMT_PX, c,
            "middle", "bold", halo=False)
        txt(x, y+t+TR.MARK_NAME_Y, m["short"], TR.MARK_NAME_PX, c,
            "middle", "bold", halo=False)

    # The four anchors. Same four on every diagram, always: they are what lets a
    # reader lay two panels side by side. Value above, name below, percentage
    # lost beneath the name — every sum on the line happens here.
    for i, a in enumerate(anchors):
        x = a["x"]
        add(f'<circle cx="{x:.0f}" cy="{TR.BY}" r="{TR.ANCHOR_R}" '
            f'fill="{TR.AGILIAN_BLUE}"/>')
        txt(x, TR.BY+TR.ANCHOR_VAL_Y, f"${a['value']:.2f}", TR.ANCHOR_VAL_PX,
            TR.INK, "middle", "bold", halo=False)
        lines = cfg.cp0_label if i == 0 else a["name"]
        for k, ln in enumerate(lines):
            txt(x, TR.BY+TR.ANCHOR_NAME_Y+k*TR.ANCHOR_NAME_LEAD, ln,
                TR.ANCHOR_NAME_PX, TR.INK, "middle", "bold", halo=False)
        if a["value"] < 99.99:
            py = (TR.BY + TR.ANCHOR_NAME_Y + (len(lines)-1)*TR.ANCHOR_NAME_LEAD
                  + TR.ANCHOR_PCT_Y)
            # Measured from the HUNDRED, which is struck at the state agency,
            # not from what enters. D-75, JW 18 September: the vaccine money is
            # not subtracted from the model, it was never part of it, so it must
            # not read as a loss. The provider tax limits must, and do — in
            # FY2030 the agency anchor is 98.76 and reports 1.24% lost.
            txt(x, py, f"{100-a['value']:.2f}% lost", TR.PCT_PX, TR.INK,
                "middle", "bold", halo=False)

    # Keep-out boxes for the fan solver: provider bars with their labels, and the
    # fraud terminal. A tributary terminal must not land on existing furniture.
    _obs=[]
    for p in order:
        _obs.append((barL-8, node_y[p]-26, barR+8, node_y[p]+node[p]*ys+6))
    _pin=[]
    if fraud > 0:
        # Fraud is no longer a fan participant. It sits ABOVE the HR-1 rule, so it
        # cannot be crossed by a tributary and does not need to order against
        # them; it is a keep-out box and nothing more. Its label is right-aligned
        # at the bar end and reaches back about 340 units.
        _obs.append((barR-340, _fy-24, barR+8, _fy+20))
    # The HR-1 rule sits BELOW everything the flow draws, so it can no longer cut
    # through the Rx drugs fan (JW, 2026-09-04). Derived, never a literal: the
    # flow's own lowest point decides where the HR-1 zone starts.
    _hr1_rule = max(node_y[order[-1]]+node[order[-1]]*ys, ffs_y+ffs*ys) + (
        76 if fraud > 0 else 30)
    return svg, (_draw_hr1(cfg, bites, ys, TB, _obs, _pin, _hr1_rule)
                 + _draw_ben_key(_key_at)
                 + _draw_absent(cfg, xBE[0]+20, _abs_y))


def _draw_ben_key(at):
    """The beneficiary overlay's key, drawn into the OVERLAY layer.

    It reads below the pies, beside the bars it explains. That puts it in the
    x-range the HR-1 fan's sub-labels run into — directed payment caps reaches
    x=1822 against a key starting at 1780 — and the fan is composited over the
    base, so drawn in the base it came out with a line of the fan's text through
    it. Same lesson as S-087: what explains the artifact draws last.
    """
    global svg
    if not at:
        return []
    lx, ky = at
    _saved, svg = svg, []
    rect(lx, ky-10, 34, 10, "#8B5A5A")
    _h = "dollars out of this service under P.L. 119-21, against prior law"
    lbg(lx+42, ky, _h, 12, "start")
    txt(lx+42, ky, _h, 12, "#8B5A5A", "start", "bold", halo=False)
    _s = "all six bars share one scale; it is not the flow's scale (bar shown = $1.00)"
    lbg(lx, ky+18, _s, 10.5, "start")
    txt(lx, ky+18, _s, 10.5, MUT, "start", halo=False, italic=True)
    out, svg = svg, _saved
    return out


def _draw_absent(cfg, ax, ay):
    """The declared-absence block, drawn into the OVERLAY layer.

    It used to sit in the base svg, where the HR-1 fan's sub-labels are
    composited on top of it: on the FY2030 panel the directed-payment-caps
    sub-label runs to x=1822 and struck a line through a declaration starting at
    x=1780. A declaration another label can paint over is not a declaration, so
    this draws last and nothing can reach it (S-071).
    """
    global svg
    if not cfg.absent:
        return []
    _saved, svg = svg, []
    _ax, _ay = ax, ay

    def _dec(y, t, px, col, bold=False, ital=False):
        lbg(_ax, y, t, px, "start")
        txt(_ax, y, t, px, col, "start", "bold" if bold else None,
            halo=False, italic=ital)
    _dec(_ay, "NOT SHOWN, and not estimated:", 13, "#8B5A5A", bold=True)
    for _i, _a in enumerate(cfg.absent):
        _dec(_ay+26+_i*22, "\u2022  "+_a, 12, MUT)
    _dec(_ay+26+len(cfg.absent)*22+14,
         "Absent data is left absent. Filling a gap with a share",
         11, MUT, ital=True)
    _dec(_ay+26+len(cfg.absent)*22+30,
         "would produce a modelled figure wearing a measured figure's clothes.",
         11, MUT, ital=True)
    out, svg = svg, _saved
    return out


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
def _draw_hr1(cfg, bites, ys, TB, obstacles=(), pinned=(), rule_y=788.0):
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
    add(f'<line x1="330" y1="{rule_y:.1f}" x2="1560" y2="{rule_y:.1f}" stroke="{WARM}" '
        f'stroke-width="1.1" stroke-dasharray="7 5" stroke-opacity="0.7"/>')
    txt(336,rule_y-8,"HR-1 TAKES THESE OUT",11,WARM,"start","bold",halo=False)
    # Solve the fan: terminals are placed so no tributary crosses another
    # (STYLE_GUIDE 2.9). Nothing here is hand-positioned.
    items=[]
    for name,xb,yb,v in bites:
        xt,sub = cfg.hr1_term[name]
        assert xt > xb, f"{name}: terminal {xt} is upstream of its bite {xb} (S-057)"
        th=max(v*ys,3.4)
        items.append(dict(name=name, label=OUTFLOWS_label(name), amt=v,
                          xb=xb, xt=xt, th=th, sub=sub,
                          y_src=(yb-v*ys)+th/2,
                          anchor=OUTFLOWS.get(name,{}).get("label_side")))
    # Tributaries that share a terminal column stack CONTIGUOUSLY there, so the
    # reader can add their thicknesses by eye and get the column's subtraction.
    # Their labels become a keyed list beside the stack rather than a block under
    # each terminal, which is what makes the stack fit at all.
    from collections import defaultdict
    grp=defaultdict(list)
    for it in items: grp[round(it["xt"])].append(it)
    # NEVER MERGE FANNING TRIBUTARIES AT THEIR TERMINATION POINTS (JW,
    # 2026-09-04). Tributaries sharing a terminal column used to be stacked
    # contiguously at one point so a reader could add their thicknesses by eye
    # and recover the column's subtraction. That reason is now served by the
    # decrement marker on the number line, and it cost the thing the audience
    # actually wants: each regulation's own dollars and cents, on its own
    # terminal. Every tributary is placed by the solver, individually.
    STACKS={}
    solo=list(items)
    YT, ANCH, fan_warn, COMPACT = fan_rows(solo + list(pinned), top=rule_y+18,
                                           obstacles=obstacles)
    for w in fan_warn:
        print(f"  WARNING  fan layout: {w}")
    _x = fan_crossings(solo + list(pinned), YT)
    assert not _x, ("tributaries cross and the solver did not resolve it: "
                    + "; ".join(f"{a} x {b}" for a, b in _x) + " (STYLE_GUIDE 2.9)")
    for name,xb,yb,v in bites:
        it=next(i for i in items if i["name"]==name)
        xt,sub,th = it["xt"], it["sub"], it["th"]
        yt=YT[name]
        y0=yb-v*ys                      # flush with the edge (S-057)
        band(xb,xt,y0,yt,th,th,WARM,0.74)
        xm=(xb+xt)/2
        add(f'<path d="M{xb:.1f},{y0:.1f} C{xm:.1f},{y0:.1f} {xm:.1f},{yt:.1f} {xt:.1f},{yt:.1f} '
            f'L{xt:.1f},{yt+th:.1f} C{xm:.1f},{yt+th:.1f} {xm:.1f},{y0+th:.1f} {xb:.1f},{y0+th:.1f} Z" '
            f'fill="url(#hr1hatch)"/>')
        if round(xt) in STACKS:
            continue                      # stacked group is labelled as a list below
        rect(xt,yt,6,max(th,4),WARMD)
        an=ANCH[name]; lx=xt-8 if an=="end" else xt
        # A declared vertical nudge for a label block, in the rare case where two
        # tributaries terminate close enough that their blocks read as one. It
        # moves the WORDS only: the terminal, the ribbon and the marker on the
        # number line all stay where the geometry put them.
        ly=yt+max(th,4)+15+float(OUTFLOWS.get(name,{}).get("label_dy",0))
        _lab = it["label"]
        # The amount rides the name's line where the solver folded this row, and
        # sits under the sub-label where it did not. Either way it stays inside
        # this tributary's own block, under this tributary's own terminal, so it
        # cannot read as belonging to the row beneath.
        _amt = f"\u2212${v:.2f}"
        if name in COMPACT:
            _head = f"{_lab}  {_amt}"
            lbg(lx,ly,_head,12,an)
            txt(lx,ly,_head,12,WARMD,an,"bold",halo=False)
            lbg(lx,ly+14,sub,10,an)
            txt(lx,ly+14,sub,10,MUT,an,halo=False,italic=True)
        else:
            lbg(lx,ly,_lab,12,an);   txt(lx,ly,_lab,12,WARMD,an,"bold",halo=False)
            lbg(lx,ly+14,sub,10,an); txt(lx,ly+14,sub,10,MUT,an,halo=False,italic=True)
            lbg(lx,ly+28,_amt,12,an)
            txt(lx,ly+28,_amt,12,WARM,an,"bold",halo=False)
    # keyed list beside each contiguous stack
    for k,v in STACKS.items():
        y0=YT[v[0]["name"]]; tot=sum(i["th"] for i in v)
        rect(k,y0,7,tot,WARMD)
        ly=y0
        for it in v:
            amt=next(b[3] for b in bites if b[0]==it["name"])
            add(f'<line x1="{k+9:.0f}" y1="{ly+it["th"]/2:.1f}" x2="{k+22:.0f}" '
                f'y2="{ly+14:.1f}" stroke="{WARMD}" stroke-width="0.9" stroke-opacity="0.6"/>')
            lbg(k+26,ly+18,f"{it['name']}  \u2212${amt:.2f}",12,"start")
            txt(k+26,ly+18,f"{it['name']}  \u2212${amt:.2f}",12,WARMD,"start","bold",halo=False)
            lbg(k+26,ly+31,it["sub"],10,"start")
            txt(k+26,ly+31,it["sub"],10,MUT,"start",halo=False,italic=True)
            ly+=max(it["th"],34)
    out, svg = svg, _saved
    return out
