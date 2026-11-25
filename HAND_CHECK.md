# Hand check of the test case

```
HAND CHECK – STEEL BEAM (test case)
Simply supported steel beam, S355, uniform load over the full span

1. INPUT DATA
   Span, L                       = 4.0 m  (4000 mm)
   Floor width carried           = 3.0 m
   Floor permanent load          = 1.5 kN/m²
   Floor variable (imposed) load = 1.5 kN/m²
   Wall load above               = 6.0 kN/m
   Self weight allowance         = 0.5 kN/m
   Steel: fy = 355 N/mm², E = 210,000 N/mm², γM0 = 1.0

2. LINE LOADS ON THE BEAM
   Permanent:  gk = (1.5 × 3.0) + 6.0 + 0.5 = 11.0 kN/m
   Variable:   qk = 1.5 × 3.0               =  4.5 kN/m

3. ULTIMATE DESIGN LOAD (Eurocode factors)
   wd = 1.35 gk + 1.5 qk
      = (1.35 × 11.0) + (1.5 × 4.5)
      = 14.85 + 6.75 = 21.6 kN/m

4. DESIGN FORCES
   Max bending moment (midspan):  M_Ed = wd L² / 8 = 21.6 × 4.0² / 8 = 43.2 kNm
   Max shear force (supports):    V_Ed = wd L / 2  = 21.6 × 4.0 / 2  = 43.2 kN

5. SECTION CHOSEN: 152x89x16 UKB
   (British Steel datasheet values)
   Depth h = 152.4 mm, web thickness tw = 4.5 mm
   Iy = 834 cm⁴, Wpl,y = 123 cm³

6. BENDING CHECK
   M_Rd = Wpl × fy / γM0
        = 123,000 mm³ × 355 N/mm²
        = 43,665,000 Nmm = 43.7 kNm
   Utilisation = 43.2 / 43.7 = 0.99 (99%)   → PASS

7. SHEAR CHECK
   Shear area (simplified) Av = h × tw = 152.4 × 4.5 = 685.8 mm²
   V_Rd = Av × fy / (√3 × γM0)
        = 685.8 × 355 / 1.732
        = 140,600 N = 140.6 kN
   Utilisation = 43.2 / 140.6 = 0.31 (31%)  → PASS

8. DEFLECTION CHECK (variable load only, limit span/360)
   δ = 5 qk L⁴ / (384 E I)
     = 5 × 4.5 × 4000⁴ / (384 × 210,000 × 834 × 10⁴)
     = 8.6 mm
   (qk = 4.5 kN/m = 4.5 N/mm;  I = 834 cm⁴ = 834 × 10⁴ mm⁴)
   Limit = L / 360 = 4000 / 360 = 11.1 mm
   Utilisation = 8.6 / 11.1 = 0.77 (77%)    → PASS

9. WHY NOT A LIGHTER BEAM?
   Next lightest is 127x76x13 UKB (Wpl,y = 84 cm³):
   M_Rd = 84,000 × 355 = 29.8 kNm < 43.2 kNm → FAILS in bending

10. CONCLUSION
   152x89x16 UKB is the lightest section in the table that passes all three checks.
   Bending governs (99%). The hand results match the program output exactly.

Assumptions: simply supported, full span UDL, compression flange fully
restrained (no lateral torsional buckling), Class 1/2 section, simplified
shear area h × tw. For demonstration of calculation automation only.
```
