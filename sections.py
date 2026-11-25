"""UK Beam (UKB) section properties, S355 steel.
Values from the British Steel UB datasheet (BS EN 10365:2017), checked 25 Nov 2026.
h = depth (mm), tw = web thickness (mm), Iy = second moment of area (cm^4),
Wpl = plastic section modulus about the major axis (cm^3).
"""

SECTIONS = [
    {"name": "127x76x13 UKB",  "mass": 13.0, "h": 127.0, "tw": 4.0, "Iy": 473,   "Wpl": 84},
    {"name": "152x89x16 UKB",  "mass": 16.0, "h": 152.4, "tw": 4.5, "Iy": 834,   "Wpl": 123},
    {"name": "178x102x19 UKB", "mass": 19.0, "h": 177.8, "tw": 4.8, "Iy": 1356,  "Wpl": 171},
    {"name": "203x102x23 UKB", "mass": 23.1, "h": 203.2, "tw": 5.4, "Iy": 2105,  "Wpl": 234},
    {"name": "254x102x22 UKB", "mass": 22.0, "h": 254.0, "tw": 5.7, "Iy": 2841,  "Wpl": 259},
    {"name": "203x133x25 UKB", "mass": 25.1, "h": 203.2, "tw": 5.7, "Iy": 2340,  "Wpl": 258},
    {"name": "254x102x25 UKB", "mass": 25.2, "h": 257.2, "tw": 6.0, "Iy": 3415,  "Wpl": 306},
    {"name": "305x102x25 UKB", "mass": 24.8, "h": 305.1, "tw": 5.8, "Iy": 4455,  "Wpl": 342},
    {"name": "203x133x30 UKB", "mass": 30.0, "h": 206.8, "tw": 6.4, "Iy": 2896,  "Wpl": 314},
    {"name": "254x146x31 UKB", "mass": 31.1, "h": 251.4, "tw": 6.0, "Iy": 4413,  "Wpl": 393},
    {"name": "254x146x37 UKB", "mass": 37.0, "h": 256.0, "tw": 6.3, "Iy": 5537,  "Wpl": 483},
    {"name": "305x127x37 UKB", "mass": 37.0, "h": 304.4, "tw": 7.1, "Iy": 7171,  "Wpl": 539},
    {"name": "305x165x40 UKB", "mass": 40.3, "h": 303.4, "tw": 6.0, "Iy": 8503,  "Wpl": 623},
    {"name": "356x171x45 UKB", "mass": 45.0, "h": 351.4, "tw": 7.0, "Iy": 12195, "Wpl": 783},
]
