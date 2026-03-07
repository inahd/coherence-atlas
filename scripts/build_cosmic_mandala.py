import csv
import math
from pathlib import Path

BASE = Path("/opt/atlas")
COSMO = BASE / "datasets" / "cosmology"
OUT = BASE / "memory" / "cosmic_mandala.html"

WIDTH = 1800
HEIGHT = 1800
CX = WIDTH // 2
CY = HEIGHT // 2

R_BINDU = 8
R_GUNA = 120
R_ELEMENT = 220
R_GRAHA = 360
R_NAK = 620

def read_csv(path):
    with open(path, newline="", encoding="utf-8", errors="ignore") as f:
        return list(csv.DictReader(f))

def polar(angle_deg, radius):
    a = math.radians(angle_deg - 90)
    return (CX + radius * math.cos(a), CY + radius * math.sin(a))

def text(x, y, s, size=14, fill="#ddd", anchor="middle", weight="normal"):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-family="Arial, sans-serif" font-weight="{weight}">{s}</text>'

def circle(x, y, r, fill, stroke="none", sw=1, title=None):
    t = f"<title>{title}</title>" if title else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}">{t}</circle>'

def line(x1, y1, x2, y2, stroke="#666", sw=1, opacity=0.35):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>'

def ring(radius, stroke="#333", sw=1):
    return f'<circle cx="{CX}" cy="{CY}" r="{radius}" fill="none" stroke="{stroke}" stroke-width="{sw}" opacity="0.6"/>'

def polygon(points, fill="none", stroke="#666", sw=2, opacity=0.8):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>'

# Load data
nak_rows = read_csv(COSMO / "nakshatra_master.csv")
deity_rows = read_csv(COSMO / "nakshatra_deities.csv")
graha_rows = read_csv(COSMO / "grahas.csv")
guna_rows = read_csv(COSMO / "gunas.csv")
elem_rows = read_csv(COSMO / "mahabhutas.csv")

deity_by_nak = {r["nakshatra"]: r["deity"] for r in deity_rows}
graha_by_nak = {}
# classical ruler cycle aligned with master dataset order
graha_cycle = [
    "Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury",
    "Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury",
    "Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury",
]
for i, r in enumerate(nak_rows):
    graha_by_nak[r["nakshatra"]] = graha_cycle[i]

# Use exactly 3 gunas and 5 elements
gunas = [r["name"] for r in guna_rows][:3]
elements = [r["name"] for r in elem_rows][:5]

# Positions
graha_order = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]
graha_pos = {}
for i, g in enumerate(graha_order):
    ang = i * (360.0 / len(graha_order))
    graha_pos[g] = polar(ang, R_GRAHA)

nak_pos = {}
for i, r in enumerate(nak_rows):
    name = r["nakshatra"]
    ang = i * (360.0 / len(nak_rows))
    nak_pos[name] = polar(ang, R_NAK)

guna_points = []
for i, g in enumerate(gunas):
    ang = i * 120.0
    guna_points.append(polar(ang, R_GUNA))

element_points = []
for i, e in enumerate(elements):
    ang = i * (360.0 / len(elements))
    element_points.append(polar(ang, R_ELEMENT))

parts = []
parts.append(f'''<html>
<head>
<meta charset="utf-8">
<title>Atlas Cosmic Mandala</title>
<style>
body {{ margin:0; background:#0f1117; color:#eee; }}
svg {{ width:100vw; height:100vh; display:block; background:#0f1117; }}
</style>
</head>
<body>
<svg viewBox="0 0 {WIDTH} {HEIGHT}">
''')

# Background rings
parts.append(ring(R_GUNA, "#3a3a3a"))
parts.append(ring(R_ELEMENT, "#3a3a3a"))
parts.append(ring(R_GRAHA, "#3a3a3a"))
parts.append(ring(R_NAK, "#3a3a3a"))

# Element pentagon
parts.append(polygon(element_points, fill="none", stroke="#556b8d", sw=2, opacity=0.8))

# Guna triangle
parts.append(polygon(guna_points, fill="none", stroke="#8d6a2f", sw=3, opacity=0.9))

# Bindu
parts.append(circle(CX, CY, R_BINDU, "#f5d76e", stroke="#fff2", sw=1, title="Bindu"))
parts.append(text(CX, CY - 18, "Bindu", 15, "#f5d76e", "middle", "bold"))

# Guna labels
guna_colors = {"sattva":"#d9f7a1", "rajas":"#ffb86c", "tamas":"#9aa0b5"}
for (x, y), g in zip(guna_points, gunas):
    parts.append(circle(x, y, 14, guna_colors.get(g, "#bbb"), stroke="#222", sw=1, title=f"Guna: {g}"))
    parts.append(text(x, y - 22, g, 14, guna_colors.get(g, "#ddd"), "middle", "bold"))

# Element labels
element_colors = {
    "ether":"#caa6ff","air":"#8be9fd","fire":"#ff6b6b","water":"#4da3ff","earth":"#7fdc6f"
}
for (x, y), e in zip(element_points, elements):
    parts.append(circle(x, y, 13, element_colors.get(e, "#bbb"), stroke="#222", sw=1, title=f"Element: {e}"))
    parts.append(text(x, y - 22, e, 13, element_colors.get(e, "#ddd"), "middle", "bold"))

# Graha nodes
graha_color = "#d4af37"
for g in graha_order:
    x, y = graha_pos[g]
    parts.append(circle(x, y, 15, graha_color, stroke="#222", sw=1, title=f"Graha: {g}"))
    parts.append(text(x, y - 24, g, 14, graha_color, "middle", "bold"))

# Nakshatra edges to grahas
for r in nak_rows:
    n = r["nakshatra"]
    g = graha_by_nak[n]
    x1, y1 = nak_pos[n]
    x2, y2 = graha_pos[g]
    parts.append(line(x1, y1, x2, y2, stroke="#6b7280", sw=1, opacity=0.28))

# Nakshatra nodes
for r in nak_rows:
    n = r["nakshatra"]
    deity = deity_by_nak.get(n, "")
    x, y = nak_pos[n]
    title = f"{n} | graha={graha_by_nak[n]} | deity={deity} | element={r['element']} | guna={r['guna']} | dosha={r['dosha']}"
    parts.append(circle(x, y, 11, "#6ea8fe", stroke="#1d3557", sw=1, title=title))
    parts.append(text(x, y - 18, n, 11, "#cfe3ff"))

# Legend
lx = 90
ly = 90
parts.append(text(lx + 30, ly, "Atlas Cosmic Mandala", 22, "#ffffff", "start", "bold"))
legend = [
    ("#f5d76e", "Bindu / center"),
    ("#d9f7a1", "Gunas triangle"),
    ("#7fdc6f", "Elements pentagon"),
    ("#d4af37", "Grahas ring"),
    ("#6ea8fe", "Nakshatra ring"),
]
for i, (c, label) in enumerate(legend):
    yy = ly + 35 + i * 28
    parts.append(circle(lx, yy - 5, 8, c))
    parts.append(text(lx + 24, yy, label, 14, "#ddd", "start"))

# Ring labels
parts.append(text(CX, CY - R_GUNA - 22, "Gunas", 16, "#d9f7a1"))
parts.append(text(CX, CY - R_ELEMENT - 22, "Mahabhutas", 16, "#7fdc6f"))
parts.append(text(CX, CY - R_GRAHA - 22, "Grahas", 16, "#d4af37"))
parts.append(text(CX, CY - R_NAK - 22, "Nakshatras", 16, "#6ea8fe"))

parts.append("</svg></body></html>")
OUT.write_text("".join(parts), encoding="utf-8")
print(f"Wrote: {OUT}")
print(f"Nakshatras: {len(nak_rows)} | Grahas: {len(graha_order)} | Gunas: {len(gunas)} | Elements: {len(elements)}")
