"""Create a one page PDF calculation sheet from the beam check results."""
from datetime import date
from fpdf import FPDF


def clean(text):
    """The built-in PDF fonts only support basic characters. Replace curly quotes
    and dashes from phone or tablet keyboards, then drop anything else unsupported."""
    swaps = {"‘": "'", "’": "'", "“": '"', "”": '"',
             "–": "-", "—": "-"}
    for old, new in swaps.items():
        text = text.replace(old, new)
    return text.encode("latin-1", "replace").decode("latin-1")


def make_report(project, beam_ref, inputs, gk, qk, wd, result):
    """Build the calc sheet and return it as PDF bytes (nothing is saved to disk)."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Steel Beam Calculation Sheet", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, clean(f"Project: {project}    Beam: {beam_ref}    Date: {date.today():%d/%m/%Y}"),
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    def section(title):
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, clean(title), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)

    def row(label, value):
        pdf.cell(95, 6, label)
        pdf.cell(0, 6, value, new_x="LMARGIN", new_y="NEXT")

    section("1. Inputs")
    row("Span", f"{inputs['span']:.2f} m")
    row("Floor width carried by beam", f"{inputs['width']:.2f} m")
    row("Floor permanent load", f"{inputs['floor_dead']:.2f} kN/m2")
    row("Floor variable (imposed) load", f"{inputs['floor_imposed']:.2f} kN/m2")
    row("Wall load above", f"{inputs['wall']:.2f} kN/m")

    section("2. Design loads")
    row("Permanent line load gk (incl. 0.5 kN/m self weight)", f"{gk:.2f} kN/m")
    row("Variable line load qk", f"{qk:.2f} kN/m")
    row("ULS design load wd = 1.35gk + 1.5qk", f"{wd:.2f} kN/m")

    if result is None:
        section("3. Result")
        row("No section in the table passes.", "Review the loads or extend the table.")
    else:
        section(f"3. Selected section: {result['section']} (S355)")
        row("Bending  M_Ed = wL^2/8", f"{result['M_ed']:.1f} kNm  vs  M_Rd = {result['M_rd']:.1f} kNm"
            f"  ({result['util_M']:.0%})")
        row("Shear  V_Ed = wL/2", f"{result['V_ed']:.1f} kN  vs  V_Rd = {result['V_rd']:.1f} kN"
            f"  ({result['util_V']:.0%})")
        row("Deflection (variable load)  5wL^4/384EI", f"{result['defl']:.1f} mm  vs  L/360 = "
            f"{result['defl_allow']:.1f} mm  ({result['util_d']:.0%})")
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, "ALL CHECKS PASS", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.multi_cell(0, 4, "Assumptions: simply supported, full span UDL, compression flange fully "
                   "restrained, Class 1/2 section, simplified shear area h x tw. Section properties "
                   "from the British Steel UB datasheet (BS EN 10365). Demonstration of calculation "
                   "automation only; not for construction without checking by a qualified engineer.")
    return bytes(pdf.output())


if __name__ == "__main__":
    from calc import design_loads, lightest_passing
    inputs = {"span": 4.0, "width": 3.0, "floor_dead": 1.5, "floor_imposed": 1.5, "wall": 6.0}
    gk, qk, wd = design_loads(inputs["span"], inputs["width"], inputs["floor_dead"],
                              inputs["floor_imposed"], inputs["wall"])
    result = lightest_passing(inputs["span"], gk, qk, wd)
    with open("beam_calc.pdf", "wb") as f:
        f.write(make_report("Test House", "B1", inputs, gk, qk, wd, result))
    print("Saved beam_calc.pdf")
