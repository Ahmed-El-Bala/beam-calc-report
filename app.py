"""Streamlit web app: steel beam sizing and PDF calculation sheet."""
import streamlit as st
from calc import design_loads, lightest_passing, check_section
from sections import SECTIONS
from report import make_report

st.set_page_config(page_title="Steel Beam Calc", page_icon="🏗️")
st.title("Steel Beam Sizing & Calc Sheet Generator")
st.caption("Sizes a simply supported steel beam (e.g. a wall knock-through) and "
           "produces a PDF calculation sheet. Simplified checks for demonstration.")

col1, col2 = st.columns(2)
with col1:
    project = st.text_input("Project name", "12 Example Road")
    beam_ref = st.text_input("Beam reference", "B1")
    span = st.number_input("Span (m)", 1.0, 10.0, 4.0, 0.1)
    width = st.number_input("Floor width carried (m)", 0.0, 10.0, 3.0, 0.1)
with col2:
    floor_dead = st.number_input("Floor permanent load (kN/m²)", 0.0, 10.0, 1.5, 0.1)
    floor_imposed = st.number_input("Floor variable load (kN/m²)", 0.0, 10.0, 1.5, 0.1)
    wall = st.number_input("Wall load above (kN/m)", 0.0, 50.0, 6.0, 0.5)

gk, qk, wd = design_loads(span, width, floor_dead, floor_imposed, wall)
st.subheader("Design loads")
st.write(f"gk = **{gk:.2f} kN/m**, qk = **{qk:.2f} kN/m**, ULS wd = **{wd:.2f} kN/m**")

result = lightest_passing(span, gk, qk, wd)
st.subheader("Result")
if result is None:
    st.error("No section in the table passes. Review the loads or extend the section table.")
else:
    st.success(f"Lightest passing section: **{result['section']}** ({result['mass']} kg/m)")
    st.write(f"Bending: {result['M_ed']:.1f} / {result['M_rd']:.1f} kNm ({result['util_M']:.0%})")
    st.write(f"Shear: {result['V_ed']:.1f} / {result['V_rd']:.1f} kN ({result['util_V']:.0%})")
    st.write(f"Deflection: {result['defl']:.1f} / {result['defl_allow']:.1f} mm ({result['util_d']:.0%})")

with st.expander("See every section checked"):
    rows = [check_section(s, span, gk, qk, wd) for s in sorted(SECTIONS, key=lambda s: s["mass"])]
    st.dataframe([{"Section": r["section"], "kg/m": r["mass"],
                   "Bending %": round(r["util_M"] * 100), "Shear %": round(r["util_V"] * 100),
                   "Deflection %": round(r["util_d"] * 100), "Pass": r["passes"]} for r in rows])

inputs = {"span": span, "width": width, "floor_dead": floor_dead,
          "floor_imposed": floor_imposed, "wall": wall}
pdf_bytes = make_report(project, beam_ref, inputs, gk, qk, wd, result)
st.download_button("Download PDF calculation sheet", data=pdf_bytes,
                   file_name=f"{beam_ref}_calc.pdf", mime="application/pdf")
