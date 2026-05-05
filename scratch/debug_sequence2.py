"""Reproduce crash with flush and step-by-step."""
import sys
import os

def p(msg):
    print(msg, flush=True)

from entoolkit import legacy
from entoolkit import (
    EN_NODECOUNT, EN_JUNCTION, EN_PIPE, EN_CHEM,
    EN_ELEVATION, EN_TANK
)

NET1 = os.path.join(os.path.dirname(__file__), "..", "tests", "networks", "Net1.inp")
NET1 = os.path.abspath(NET1)

# --- Test 1: lifecycle ---
p("=== TEST 1: lifecycle ===")
try: legacy.ENclose()
except: pass
legacy.ENopen(NET1)
legacy.ENsettitle("L1", "L2", "L3")
legacy.ENgettitle()
index = legacy.ENgetnodeindex("10")
legacy.ENsetcomment(EN_NODECOUNT, index, "Comment")
legacy.ENgetcomment(EN_NODECOUNT, index)
legacy.ENgetversion()
legacy.ENclose()
p("  OK")

# --- Test 2: network edit ---
p("=== TEST 2: network edit ===")
try: legacy.ENclose()
except: pass
legacy.ENinit()
j1 = legacy.ENaddnode("NJ1", EN_JUNCTION)
j2 = legacy.ENaddnode("NJ2", EN_JUNCTION)
t1 = legacy.ENaddnode("T1", EN_TANK)
p1 = legacy.ENaddlink("PL1", EN_PIPE, "NJ1", "NJ2")
legacy.ENsetnodeid(j1, "R_J1")
legacy.ENsetnodevalue(j1, EN_ELEVATION, 100.0)
legacy.ENsetjuncdata(j2, 50.0, 1.0, "")
legacy.ENsettankdata(t1, 100.0, 5.0, 2.0, 10.0, 20.0, 0.0, "")
legacy.ENsetpipedata(p1, 1000.0, 300.0, 100.0, 0.1)
legacy.ENsetcoord(j1, 10.0, 20.0)
legacy.ENadddemand(j1, 1.0, "", "D1")
num = legacy.ENgetnumdemands(j1)
p(f"  demands={num}, base={legacy.ENgetbasedemand(j1, num)}")
legacy.ENsetbasedemand(j1, num, 5.0)
legacy.ENdeletedemand(j1, num)
legacy.ENsetvertices(p1, [15.0, 25.0], [25.0, 35.0])
legacy.ENdeletelink(p1, 1)
legacy.ENdeletenode(j1, 1)
legacy.ENclose()
p("  OK")

# --- Test 3: simulation stepped ---
p("=== TEST 3: simulation ===")
legacy.ENopen(NET1)
legacy.ENsolveH()
legacy.ENsetqualtype(EN_CHEM, "Chlorine", "mg/L", "")
legacy.ENopenQ()
legacy.ENinitQ(0)
legacy.ENrunQ()
legacy.ENnextQ()
legacy.ENcloseQ()
legacy.ENclose()
p("  OK")

# --- Test 4: patterns and curves ---
p("=== TEST 4: patterns & curves ===")
try: legacy.ENclose()
except: pass

p("  4a: ENinit")
legacy.ENinit()

p("  4b: ENaddpattern")
p_idx = legacy.ENaddpattern("PAT_LEG")
p(f"     p_idx={p_idx}")

p("  4c: ENsetpattern")
legacy.ENsetpattern(p_idx, [1.0, 1.2, 0.8])

p("  4d: ENgetpatternlen")
assert legacy.ENgetpatternlen(p_idx) == 3

p("  4e: ENgetpatternid")
assert legacy.ENgetpatternid(p_idx) == "PAT_LEG"

p("  4f: ENsetpatternvalue")
legacy.ENsetpatternvalue(p_idx, 2, 1.5)

p("  4g: ENgetpatternvalue")
assert legacy.ENgetpatternvalue(p_idx, 2) == 1.5

p("  4h: ENdeletepattern")
legacy.ENdeletepattern(p_idx)

p("  4i: ENaddcurve")
c_idx = legacy.ENaddcurve("CURVE_LEG")
p(f"     c_idx={c_idx}")

p("  4j: ENsetcurvevalue")
legacy.ENsetcurvevalue(c_idx, 1, 10.0, 100.0)

p("  4k: ENgetcurvevalue")
x, y = legacy.ENgetcurvevalue(c_idx, 1)
p(f"     x={x}, y={y}")

p("  4l: ENgetcurvelen")
assert legacy.ENgetcurvelen(c_idx) == 1

p("  4m: ENdeletecurve")
legacy.ENdeletecurve(c_idx)

p("  4n: ENclose")
legacy.ENclose()

p("ALL DONE!")
