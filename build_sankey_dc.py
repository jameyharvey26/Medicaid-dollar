#!/usr/bin/env python3
# ===== $100 Medicaid Dollars - DC variant, national FRAMEWORK with per-payer service split =====
# FEDERAL | LOCAL | DC AGENCY | DISBURSEMENTS | PAYER | PROVIDERS.
# FFS has no payer: it splits into service streams at the agency and runs straight through the
# payer column to the providers, unchanged. Each MCO splits its care into the services it funds
# and stays colour-coded by payer into the provider bars, so each provider shows who paid for it.
# Spine: CMS-64/MACStats FY2024 DC. MCO split + payer peel: DHCF CY2023. MCO->service mix: national proxy (modeled).
import sys
SCALE = 43.72
fed, state = 73.17, 26.83
admin, medicare = 234/SCALE, 86/SCALE
mc_total = 1802/SCALE                  # all managed-care capitation (CMS-64 classes PACE + D-SNP wrap here too)
pace = 15/SCALE                         # PACE (Edenbridge) - separate capitated payer, ~order-of-magnitude
dual = 25/SCALE                         # UHC Dual Choice D-SNP, Medicaid-only wrap (MODELED, see footnote)
mco_cap = mc_total - pace - dual        # the four comprehensive/CASSIP plans
ffs = 2250/SCALE
disbursed = 100 - admin - medicare

plan = ["HSCSN", "MedStar Family Choice DC", "Wellpoint DC", "AmeriHealth Caritas DC"]  # smallest->largest (top->bottom)
comp = ["MedStar Family Choice DC", "Wellpoint DC", "AmeriHealth Caritas DC"]            # three comprehensive plans
rev    = {"AmeriHealth Caritas DC": 841.0, "Wellpoint DC": 425.3, "MedStar Family Choice DC": 411.2, "HSCSN": 184.0}
clm    = {"AmeriHealth Caritas DC": 755.5, "Wellpoint DC": 348.5, "MedStar Family Choice DC": 379.6, "HSCSN": 154.4}
owner  = {"AmeriHealth Caritas DC": "AmeriHealth Caritas", "Wellpoint DC": "Elevance",
          "MedStar Family Choice DC": "MedStar Health", "HSCSN": "Children's National"}
# Anchor HSCSN at its ACTUAL Medicaid (CASSIP) capitation: its $184M is Medicaid-only, whereas the
# comprehensive plans' revenue still carries Alliance (local) dollars. Splitting all four by raw
# revenue under-weights HSCSN, so fix it at $184M and split the Medicaid residual among the three.
cap = {"HSCSN": 184.0/SCALE}
comp_resid = mco_cap - cap["HSCSN"]; comp_revT = sum(rev[p] for p in comp)
for p in comp: cap[p] = rev[p]/comp_revT*comp_resid
care = {p: cap[p]*(clm[p]/rev[p]) for p in plan}
adm  = {p: cap[p]-care[p] for p in plan}
mco_care = sum(care.values()); mco_adm = sum(adm.values())

order = ["Long-term care", "Physicians & clinics", "Hospitals", "Wrap around services", "Rx drugs"]
ffs_n = {"Long-term care": 1236/SCALE, "Physicians & clinics": 406/SCALE, "Hospitals": 297/SCALE,
         "Wrap around services": 222/SCALE, "Rx drugs": 89/SCALE}
natmix = {"Long-term care": 8.82, "Hospitals": 9.98, "Physicians & clinics": 9.76+6.03,
          "Wrap around services": 8.38, "Rx drugs": 2.38}
mixT = sum(natmix.values()); mix = {p: natmix[p]/mixT for p in order}
mco_c = {p: {s: care[p]*mix[s] for s in order} for p in plan}     # MCO p -> service s
node = {s: ffs_n[s] + sum(mco_c[p][s] for p in plan) for s in order}
dual_ltc, dual_wrap = dual*0.75, dual*0.25                        # duals: Medicare covers acute; Medicaid = LTSS + dental/BH wrap
node["Long-term care"] += pace + dual_ltc                         # PACE 100% to LTC; D-SNP LTSS share
node["Wrap around services"] += dual_wrap                         # D-SNP dental/behavioral wrap

def ap(a,b,t=0.1): return abs(a-b)<=t
checks=[("sources=100",ap(fed+state,100)),("uses=100",ap(admin+medicare+mc_total+ffs,100)),
        ("lanes=disbursed",ap(mc_total+ffs,disbursed)),("MCO cap sums",ap(sum(cap.values()),mco_cap)),
        ("FFS nodes=FFS",ap(sum(ffs_n.values()),ffs)),("care+adm=cap",ap(mco_care+mco_adm,mco_cap)),
        ("nodes=care delivered",ap(sum(node.values()),ffs+mco_care+pace+dual))]
print("="*56,"\nDC FRAMEWORK + per-payer service split\n"+"="*56)
ok=True
for n,p in checks: print(f"  {'PASS' if p else 'FAIL'}: {n}"); ok=ok and p
if not ok: sys.exit("balance failed")

W,H,cY,ys,bw = 2480,1160,560,4.8,18
FED,STATE,DOLLAR="#2f5d74","#9bb8c4","#1a6b40"
FFSCOL,ADMIN,MEDI,RETAIN="#7d97a8","#9a9a9a","#9aa0a6","#5e5e5e"
MCOCOL={"AmeriHealth Caritas DC":"#2f7d77","Wellpoint DC":"#3a6ea5","MedStar Family Choice DC":"#7a5a92","HSCSN":"#c08a3e"}
PACECOL="#b0436b"
DUALCOL="#7a5230"
INK,MUT,BG,LINE="#272727","#6f6f6f","#faf8f3","#e2dccf"
svg=[]
def add(s): svg.append(s)
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def band(x0,x1,y0,y1,h0,h1,fill,op=0.78):
    xm=(x0+x1)/2
    add(f'<path d="M{x0:.1f},{y0:.1f} C{xm:.1f},{y0:.1f} {xm:.1f},{y1:.1f} {x1:.1f},{y1:.1f} L{x1:.1f},{y1+h1:.1f} C{xm:.1f},{y1+h1:.1f} {xm:.1f},{y0+h0:.1f} {x0:.1f},{y0+h0:.1f} Z" fill="{fill}" fill-opacity="{op}" stroke="{fill}" stroke-opacity="0.35" stroke-width="0.5"/>')
def rect(x,y,w,h,fill,op=1.0,rx=2): add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{max(h,0.5):.1f}" rx="{rx}" fill="{fill}" fill-opacity="{op}"/>')
def txt(x,y,s,size=13,fill=INK,anchor="start",weight="normal",halo=True,italic=False):
    it=' font-style="italic"' if italic else ''; po=' paint-order="stroke" stroke="#faf8f3" stroke-width="2.2" stroke-linejoin="round"' if halo else ''
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{it}{po}>{esc(s)}</text>')
def lbg(x,y,s,size=12.5,anchor="start",pad=4):
    w=len(s)*size*0.56+pad*2; h=size+pad*1.5; xx=x-pad if anchor=="start" else (x-w/2 if anchor=="middle" else x-w+pad)
    add(f'<rect x="{xx:.1f}" y="{y-size:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" fill="{BG}" fill-opacity="0.82"/>')

xFED,xLOC,xAGN,xDI,xPA,xPR = 110,380,690,1130,1450,1890
add(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>')
txt(50,44,"$100 of DC Medicaid Spending",22,INK,"start","bold",halo=False)
txt(50,68,"District of Columbia variant - national framework - each payer colour-coded into the services it funds - spine CMS-64/MACStats FY2024, payer split DHCF CY2023",12,MUT,"start",halo=False,italic=True)
heads=[("FEDERAL","money from above",xFED),("LOCAL (DC)","fed + local in parallel",xLOC),("DC AGENCY","the $100 combined",xAGN),
       ("DISBURSEMENTS","FFS splits here; capitation to MCOs",xDI),("PAYER","MCOs; FFS passes through",xPA),("PROVIDERS","services, by who paid",xPR)]
for name,sub,x in heads:
    txt(x,100,name,13.5,INK,"start","bold",halo=False); txt(x,116,sub,10.5,MUT,"start",halo=False,italic=True)
    add(f'<line x1="{x}" y1="126" x2="{x}" y2="{H-128}" stroke="{LINE}" stroke-width="1"/>')
add(f'<line x1="50" y1="126" x2="{W-30}" y2="126" stroke="{LINE}" stroke-width="1.2"/>')

# ---- sources ----
T0=cY-100*ys/2; fed_lane=(T0,T0+fed*ys); st_lane=(fed_lane[1],T0+100*ys)
fed_top,st_top=170,860
rect(xFED,fed_top,bw,fed*ys,FED); rect(xFED,st_top,bw,state*ys,STATE)
lbg(xFED,fed_top-9,"Federal  $73.17",13); txt(xFED,fed_top-9,"Federal  $73.17",13,FED,"start","bold",halo=False)
lbg(xFED,st_top+state*ys+17,"Local (DC)  $26.83",13); txt(xFED,st_top+state*ys+17,"Local (DC)  $26.83",13,"#5f7f8c","start","bold",halo=False)
band(xFED+bw,xAGN,fed_top,fed_lane[0],fed*ys,fed*ys,FED,0.8); band(xFED+bw,xAGN,st_top,st_lane[0],state*ys,state*ys,STATE,0.8)

# ---- agency $100 + peels ----
rect(xAGN,T0,bw,100*ys,DOLLAR)
pA,pB=xAGN+150,xAGN+300
band(xAGN+bw,pA,T0,T0,100*ys,100*ys,DOLLAR,0.82)
top2=T0+admin*ys; band(pA,pB,top2,top2,(100-admin)*ys,(100-admin)*ys,DOLLAR,0.82)
top3=top2+medicare*ys; band(pB,xDI,top3,top3,(100-admin-medicare)*ys,(100-admin-medicare)*ys,DOLLAR,0.82)
# administration peel SPLIT THREE WAYS by match rate (ILLUSTRATIVE split pending CMS-64/APD pull)
adm_parts=[("Operating administration",3.60,"50% federal","#9a9a9a"),
           ("Systems M&O",1.20,"75% federal","#6f9a86"),
           ("Systems DDI (one-time builds)",0.55,"90% federal","#3f9a64")]
aslice=T0; term_x=pA+55; term_y=[88,128,168]
for i,(nm,val,rate,col) in enumerate(adm_parts):
    h=val*ys
    band(pA,term_x,aslice,term_y[i],h,h,col,0.85); rect(term_x,term_y[i],5,max(h,3),col)
    lbg(term_x+12,term_y[i]+6,f"{nm}  ${val:.2f}",11); txt(term_x+12,term_y[i]+6,f"{nm}  ${val:.2f}",11,col,"start","bold",halo=False)
    txt(term_x+12,term_y[i]+19,rate,9.5,MUT,"start",halo=False,italic=True)
    aslice+=h
txt(term_x+12,term_y[2]+38,"Illustrative split - needs CMS-64/APD",9.5,MUT,"start",halo=False,italic=True)
band(pB,pB+120,top2,250,medicare*ys,medicare*ys,MEDI,0.85); rect(pB+120,250,5,max(medicare*ys,4),MEDI)
lbg(pB+132,246,"Medicare premiums  $1.97",12); txt(pB+132,246,"Medicare premiums  $1.97",12,"#5f6166","start","bold",halo=False)
lbg(pB+132,261,"duals - back to federal",10); txt(pB+132,261,"duals - back to federal",10,MUT,"start",halo=False,italic=True)
txt(xAGN+bw/2,cY-3,"$100",15,"#fff","middle","bold",halo=False); txt(xAGN+bw/2,cY+14,"DC Medicaid",11,"#fff","middle","bold",halo=False)

# ---- disbursements: MCO capitation (top) + FFS split into 5 service lanes (bottom) ----
mco_y=top3; ffs_y=top3+mc_total*ys
rect(xDI,mco_y,bw,mc_total*ys,"#3f8f8a")
lbg(xDI+22,mco_y+mc_total*ys/2+4,"Managed care  $41.22",12); txt(xDI+22,mco_y+mc_total*ys/2+4,"Managed care  $41.22",12,"#1f5b57","start","bold",halo=False)
# FFS splits right here into 5 service sub-lanes
ffs_src={}; yk=ffs_y
for s in order:
    h=ffs_n[s]*ys; rect(xDI,yk,bw,h,FFSCOL); ffs_src[s]=(yk,h); yk+=h
lbg(xDI+22,ffs_y+ffs*ys/2+4,"Fee-for-service  $51.46  (splits by service)",11.5); txt(xDI+22,ffs_y+ffs*ys/2+4,"Fee-for-service  $51.46  (splits by service)",11.5,"#36505f","start","bold",halo=False)

# ---- provider nodes: each a stack of [FFS, AMH, WLP, MED, HSC], coloured by payer ----
gap=18; htot=sum(node[s] for s in order)*ys+(len(order)-1)*gap; ntop=cY-htot/2
ny={}; y=ntop
for s in order: ny[s]=y; y+=node[s]*ys+gap
seg_y={}  # seg_y[s][src] = (y, h)
for s in order:
    yy=ny[s]; seg_y[s]={}
    if s=="Long-term care":
        seg_y[s]["PACE"]=(yy,pace*ys); yy+=pace*ys
        seg_y[s]["DUAL"]=(yy,dual_ltc*ys); yy+=dual_ltc*ys
    if s=="Wrap around services":
        seg_y[s]["DUAL"]=(yy,dual_wrap*ys); yy+=dual_wrap*ys
    h=ffs_n[s]*ys; seg_y[s]["FFS"]=(yy,h); yy+=h
    for p in plan:
        h=mco_c[p][s]*ys; seg_y[s][p]=(yy,h); yy+=h

# ---- FFS: straight from agency through payer column to providers (unchanged) ----
for s in order:
    sy,h=ffs_src[s]; ty,_=seg_y[s]["FFS"]
    band(xDI+bw,xPR,sy,ty,h,h,FFSCOL,0.55)

# ---- PAYER: capitation -> PACE (smallest, top) then 4 MCO bars ascending; peel admin; split to services ----
band(xDI+bw,xPA,mco_y,mco_y,mc_total*ys,mc_total*ys,"#3f8f8a",0.4)
cur=mco_y; adm_run=232
# PACE first (smallest): separate capitated payer, 100% to long-term care (no admin peel shown)
hpace=pace*ys; rect(xPA,cur,bw,hpace,PACECOL)
pty,_=seg_y["Long-term care"]["PACE"]
band(xPA+bw,xPR,cur,pty,hpace,hpace,PACECOL,0.7)
lbg(xPA+bw+8,cur-17,f"PACE  ${pace:.2f} -> LTC  (Edenbridge)",9.5); txt(xPA+bw+8,cur-17,f"PACE  ${pace:.2f} -> LTC  (Edenbridge)",9.5,PACECOL,"start","bold",halo=False)
cur+=hpace
# UHC Dual Choice D-SNP: Medicaid-only wrap for duals (Medicare pays acute); splits to LTSS + dental/BH wrap
hdual=dual*ys; rect(xPA,cur,bw,hdual,DUALCOL)
csrc=cur
for s,amt in (("Long-term care",dual_ltc),("Wrap around services",dual_wrap)):
    ty,_=seg_y[s]["DUAL"]; band(xPA+bw,xPR,csrc,ty,amt*ys,amt*ys,DUALCOL,0.7); csrc+=amt*ys
lbg(xPA+bw+8,cur-5,f"UHC Dual Choice D-SNP  ${dual:.2f} -> LTSS + wrap  (modeled)",9.5); txt(xPA+bw+8,cur-5,f"UHC Dual Choice D-SNP  ${dual:.2f} -> LTSS + wrap  (modeled)",9.5,DUALCOL,"start","bold",halo=False)
cur+=hdual
for p in plan:    # plan is smallest->largest: HSCSN, MedStar, Wellpoint, AmeriHealth
    hcap=cap[p]*ys; rect(xPA,cur,bw,hcap,MCOCOL[p])
    txt(xPA+bw+8,cur+hcap/2-2,f"{p}  ${cap[p]:.2f}",11.5,INK,"start","bold",halo=False)
    txt(xPA+bw+8,cur+hcap/2+12,f"${cap[p]*SCALE:.0f}M cap - {owner[p]}",9.5,MUT,"start",halo=False,italic=True)
    ha=adm[p]*ys; band(xPA+bw,xPA+bw+92,cur,adm_run,ha,ha,RETAIN,0.78); adm_run+=ha
    csrc=cur+ha  # care region begins below the peeled admin slice
    for s in order:
        h=mco_c[p][s]*ys; ty,_=seg_y[s][p]
        band(xPA+bw,xPR,csrc,ty,h,h,MCOCOL[p],0.6); csrc+=h
    cur+=hcap
rect(xPA+bw+92,232,5,max(mco_adm*ys,4),RETAIN)
lbg(xPA+bw+102,228,"MCO plan admin & margin  $4.96",11.5); txt(xPA+bw+102,228,"MCO plan admin & margin  $4.96",11.5,RETAIN,"start","bold",halo=False)
lbg(xPA+bw+102,243,"per-plan claims/revenue, DHCF CY2023 (MLR 82-92%)",9.5); txt(xPA+bw+102,243,"per-plan claims/revenue, DHCF CY2023 (MLR 82-92%)",9.5,MUT,"start",halo=False,italic=True)

# ---- provider bars (stacked, coloured by payer) + labels ----
for s in order:
    yb=ny[s]; total=node[s]
    rect(xPR,seg_y[s]["FFS"][0],150,seg_y[s]["FFS"][1],FFSCOL)
    for p in plan: rect(xPR,seg_y[s][p][0],150,seg_y[s][p][1],MCOCOL[p])
    if "PACE" in seg_y[s]: rect(xPR,seg_y[s]["PACE"][0],150,seg_y[s]["PACE"][1],PACECOL)
    if "DUAL" in seg_y[s]: rect(xPR,seg_y[s]["DUAL"][0],150,seg_y[s]["DUAL"][1],DUALCOL)
    extra=f"  + PACE ${pace:.2f} + D-SNP ${dual_ltc:.2f}" if s=="Long-term care" else (f"  + D-SNP ${dual_wrap:.2f}" if s=="Wrap around services" else "")
    txt(xPR+160,yb+node[s]*ys/2-2,f"{s}   ${total:.2f}",13,INK,"start","bold",halo=False)
    txt(xPR+160,yb+node[s]*ys/2+13,f"FFS ${ffs_n[s]:.2f}  -  MCOs ${sum(mco_c[p][s] for p in plan):.2f} (modeled){extra}",10,MUT,"start",halo=False,italic=True)

# ---- legend ----
lx,lyy=50,H-104
txt(lx,lyy-8,"WHO PAYS (colour):",10.5,INK,"start","bold",halo=False)
leg=[("Fee-for-service",FFSCOL)]+[(p,MCOCOL[p]) for p in plan]+[("PACE (Edenbridge)",PACECOL),("UHC Dual Choice D-SNP",DUALCOL)]
cx=lx
for name,c in leg:
    rect(cx,lyy,16,12,c); txt(cx+21,lyy+10,name,10.5,INK,"start",halo=False); cx+=len(name)*6.4+44

fy=H-76
txt(50,fy,"Administration ($5.35) spans 50-90% federal: routine operations are DC's LEAST-matched dollars (50%), while one-time systems builds (DDI) are its MOST (90%, matching expansion care) and ongoing systems operations (M&O) draw 75%. The three-way split shown is ILLUSTRATIVE pending a CMS-64/APD pull.",10.5,MUT,"start",halo=False,italic=True)
txt(50,fy+15,"Fee-for-service has no payer: it splits into services at the agency and runs straight through the payer column to providers, unchanged. Each MCO retains plan admin & margin "
          "(per-plan claims/revenue, DHCF CY2023) then funds the services it covers, staying colour-coded into each provider bar.",10.5,MUT,"start",halo=False,italic=True)
txt(50,fy+30,"Solid spine measured (MACStats Exhibit 17 for FFS; DHCF capitation for MCO totals). HSCSN anchored at its actual $184M Medicaid (CASSIP) capitation; three comprehensive plans split the residual. PACE (Edenbridge) "
          "and the UHC Dual Choice D-SNP are separate capitated payers carved from the lump; the D-SNP figure is MODELED Medicaid-only wrap (Medicare pays duals' acute care; most dual LTSS is still FFS in the LTC node). MCO->service split is MODELED (national mix).",10.5,MUT,"start",halo=False,italic=True)

svg_str=f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">\n'+"\n".join(svg)+"\n</svg>"
open("medicaid_dollar_sankey_DC.svg","w").write(svg_str)
open("medicaid_dollar_sankey_DC.html","w").write("<!doctype html><html><head><meta charset='utf-8'><title>$100 of DC Medicaid Spending</title><style>body{margin:0;background:#faf8f3}.wrap{max-width:2480px;margin:0 auto;padding:12px}svg{width:100%;height:auto}</style></head>"+f"<body><div class='wrap'>{svg_str}</div></body></html>")
print("Wrote medicaid_dollar_sankey_DC.html and .svg")
