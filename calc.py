"""Simply supported steel beam check (simplified, for demonstration only).

Assumptions:
- Simply supported, uniformly distributed load (UDL) over the full span.
- Compression flange fully restrained (no lateral torsional buckling check).
- Class 1 or 2 sections, so the plastic modulus is used for bending.
- Loads combined with Eurocode factors: 1.35 x permanent + 1.5 x variable.
"""
import math
from sections import SECTIONS

FY = 355.0      # yield strength of S355 steel, N/mm^2 (all flanges here are under 16 mm)
E = 210000.0    # Young's modulus of steel, N/mm^2
GAMMA_M0 = 1.0  # partial factor for resistance
SELF_WEIGHT = 0.5  # kN/m allowance; the heaviest beam in the table is 45 kg/m = 0.44 kN/m


def design_loads(span_m, width_m, floor_dead, floor_imposed, wall_load, self_weight=SELF_WEIGHT):
    """Return line loads in kN/m: (permanent gk, variable qk, ULS design load wd)."""
    gk = floor_dead * width_m + wall_load + self_weight
    qk = floor_imposed * width_m
    wd = 1.35 * gk + 1.5 * qk
    return gk, qk, wd


def check_section(sec, span_m, gk, qk, wd, defl_limit=360):
    """Check one section for bending, shear and deflection. Return a results dict."""
    M_ed = wd * span_m ** 2 / 8                      # kNm, maximum bending moment (midspan)
    V_ed = wd * span_m / 2                           # kN, maximum shear force (supports)
    M_rd = sec["Wpl"] * 1e3 * FY / GAMMA_M0 / 1e6    # kNm (Wpl cm^3 -> mm^3)
    A_v = sec["h"] * sec["tw"]                       # mm^2, simplified (conservative) shear area
    V_rd = A_v * FY / math.sqrt(3) / GAMMA_M0 / 1e3  # kN
    # Deflection under variable load only, 5wL^4/384EI
    L = span_m * 1000                                # mm
    I = sec["Iy"] * 1e4                              # mm^4
    defl = 5 * qk * L ** 4 / (384 * E * I)           # qk in kN/m equals N/mm
    defl_allow = L / defl_limit
    return {
        "section": sec["name"], "mass": sec["mass"],
        "M_ed": M_ed, "M_rd": M_rd, "util_M": M_ed / M_rd,
        "V_ed": V_ed, "V_rd": V_rd, "util_V": V_ed / V_rd,
        "defl": defl, "defl_allow": defl_allow, "util_d": defl / defl_allow,
        "passes": M_ed <= M_rd and V_ed <= V_rd and defl <= defl_allow,
    }


def lightest_passing(span_m, gk, qk, wd):
    """Return the lightest section that passes every check, or None."""
    for sec in sorted(SECTIONS, key=lambda s: s["mass"]):
        result = check_section(sec, span_m, gk, qk, wd)
        if result["passes"]:
            return result
    return None


if __name__ == "__main__":
    gk, qk, wd = design_loads(span_m=4.0, width_m=3.0, floor_dead=1.5,
                              floor_imposed=1.5, wall_load=6.0)
    print(f"gk = {gk:.2f} kN/m, qk = {qk:.2f} kN/m, wd = {wd:.2f} kN/m")
    r = lightest_passing(4.0, gk, qk, wd)
    if r is None:
        print("No section passes")
    else:
        print(f"Selected: {r['section']}")
        print(f"Bending    {r['M_ed']:.1f} / {r['M_rd']:.1f} kNm  ({r['util_M']:.0%})")
        print(f"Shear      {r['V_ed']:.1f} / {r['V_rd']:.1f} kN   ({r['util_V']:.0%})")
        print(f"Deflection {r['defl']:.1f} / {r['defl_allow']:.1f} mm   ({r['util_d']:.0%})")
