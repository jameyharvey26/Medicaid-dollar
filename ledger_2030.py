# ledger_2030.py — the FY2030 post-HR-1 ledger, per $100 of prior-law spending.
#
# Bite phases (D-64): provider tax limits leave the FEDERAL band; the four
# enrolment levers leave at the STATE AGENCY, because a person never enrolled
# generates no capitation and no claim; directed payment caps hit the CLAIMS fan
# on the capitated leg, against the three provider classes the statute names.
# Overhead is split (D-63): plan administration scales with capitation under the
# MLR floor, state administration holds at FY2024 dollars.

from tobe2030 import per100

# --- baseline ledger, prior law, per $100 ----------------------------------
B = dict(admin=5.07, medicare=2.90, mco=40.06, dual=10.89, ffs=41.08,
         mco_ret=4.41, dual_ret=1.20, earnings=0.76, mco_adm=3.81,
         dual_adm=1.04, fraud=0.15)
B_ffs_n  = {"Long-term care":19.72,"Hospitals":8.68,"Other":4.95,
            "Physicians & clinics":2.87,"Behavioral health":3.48,"Rx drugs":1.38}
B_mcoc_n = {"Long-term care":6.93,"Hospitals":7.84,"Other":6.59,
            "Physicians & clinics":7.68,"Behavioral health":4.74,"Rx drugs":1.87}
B_dualc_n= {"Long-term care":1.89,"Hospitals":2.14,"Other":1.79,
            "Physicians & clinics":2.08,"Behavioral health":1.29,"Rx drugs":0.51}
ORDER = ["Long-term care","Hospitals","Other","Physicians & clinics",
         "Behavioral health","Rx drugs"]

# --- where each lever bites -------------------------------------------------
PT   = per100["Provider tax limits"]                 # STATE GOVERNMENT
MSP  = per100["Blocked senior enrollment rule"]      # STATE AGENCY, Medicare-premium lane
DISB = (per100["Work reporting"] + per100["Six-month renewals"]
        + per100["Blocked Medicaid enrollment rule"] + per100["Everything else"])
SDP  = per100["Directed payment caps"]               # CLAIMS
TOTAL_BITE = PT + MSP + DISB + SDP


def ledger(variant):
    """Post-HR-1 ledger per $100 of prior-law FY2030 spending.

    Bite phases corrected 2026-08-29 (D-64):
      PT   leaves the FEDERAL band before the merge. Federal match never drawn.
      MSP  leaves at the STATE AGENCY, reducing the Medicare-premium lane.
      WORK, RENEW, BLOCKED, ELSE leave at the STATE AGENCY. They stop
           enrolment, so the dollar never reaches a payer lane.
      SDP  hits the CLAIMS fan, on the capitated leg, against the three
           provider classes the statute names.
    """
    admin_fixed = variant in ("holds", "mixed")
    plan_scales = variant in ("scales", "mixed")
    trunk = 100.0 - PT
    medicare = max(B["medicare"] - MSP, 0.0)
    admin = B["admin"] if admin_fixed else B["admin"] * trunk / 100.0
    STATE_COV = (per100["Work reporting"] + per100["Six-month renewals"]
                 + per100["Blocked Medicaid enrollment rule"]
                 + per100["Everything else"])
    disbursed = trunk - admin - medicare - MSP - STATE_COV
    base_lane_tot = B["mco"] + B["dual"] + B["ffs"]
    sh = {k: B[k] / base_lane_tot for k in ("mco", "dual", "ffs")}
    mco, dual, ffs = (disbursed * sh["mco"], disbursed * sh["dual"],
                      disbursed * sh["ffs"])
    if not plan_scales:
        mco_ret, dual_ret = B["mco_ret"], B["dual_ret"]
        earnings, mco_adm, dual_adm = B["earnings"], B["mco_adm"], B["dual_adm"]
        fraud = B["fraud"]
    else:
        rm, rd = mco / B["mco"], dual / B["dual"]
        mco_ret, dual_ret = B["mco_ret"] * rm, B["dual_ret"] * rd
        earnings, mco_adm = B["earnings"] * rm, B["mco_adm"] * rm
        dual_adm = B["dual_adm"] * rd
        fraud = B["fraud"] * ffs / B["ffs"]
    mco_care, dual_care = mco - mco_ret, dual - dual_ret
    claims = mco_care + dual_care + ffs
    # provider nodes, before the SDP bite
    mcoc  = {p: B_mcoc_n[p]  * mco_care / (B["mco"] - B["mco_ret"])  for p in ORDER}
    dualc = {p: B_dualc_n[p] * dual_care / (B["dual"] - B["dual_ret"]) for p in ORDER}
    ffsn  = {p: B_ffs_n[p]   * ffs / B["ffs"] for p in ORDER}
    # SDP bite: statute names inpatient + outpatient hospital, nursing facility,
    # and qualified practitioner services at academic medical centers. It is a
    # managed care arrangement, so it lands on the CAPITATED leg only.
    # Apportioned across the three named classes by capitated share. MODELLED:
    # CBO publishes no split among them (EN-21).
    NAMED = ["Hospitals", "Long-term care", "Physicians & clinics"]
    cap_named = sum(mcoc[p] + dualc[p] for p in NAMED)
    sdp_hit = {p: SDP * (mcoc[p] + dualc[p]) / cap_named for p in NAMED}
    for p in NAMED:
        f = 1.0 - sdp_hit[p] / (mcoc[p] + dualc[p])
        mcoc[p] *= f; dualc[p] *= f
    node = {p: mcoc[p] + dualc[p] + ffsn[p] for p in ORDER}
    to_prov = claims - SDP
    delivered = to_prov - fraud
    return dict(admin=admin, medicare=medicare, mco=mco, dual=dual, ffs=ffs,
                mco_ret=mco_ret, dual_ret=dual_ret, earnings=earnings,
                mco_adm=mco_adm, dual_adm=dual_adm, mco_care=mco_care,
                dual_care=dual_care, fraud=fraud, node=node, mcoc=mcoc,
                dualc=dualc, ffsn=ffsn, disbursed=disbursed, claims=claims,
                to_prov=to_prov, delivered=delivered, trunk=trunk,
                state_cov=STATE_COV, sdp_hit=sdp_hit)
