"""Reproduce the test sequence that leads to the crash.
Previous tests run: lifecycle_metadata -> network_edit -> simulation_stepped -> patterns_curves
The crash happens when running in sequence because of shared global state.
"""
from entoolkit import legacy
from entoolkit import (
    EN_NODECOUNT, EN_JUNCTION, EN_PIPE, EN_CHEM,
    EN_ELEVATION, EN_TANK, EN_BASEDEMAND
)
import os

NET1 = os.path.join(os.path.dirname(__file__), "..", "tests", "networks", "Net1.inp")
NET1 = os.path.abspath(NET1)

print("=== test_legacy_lifecycle_and_metadata ===")
try: legacy.ENclose()
except: pass
legacy.ENopen(NET1)
legacy.ENsettitle("L1", "L2", "L3")
t1, t2, t3 = legacy.ENgettitle()
print(f"  title: {t1}")
index = legacy.ENgetnodeindex("10")
legacy.ENsetcomment(EN_NODECOUNT, index, "Testing Comment")
c = legacy.ENgetcomment(EN_NODECOUNT, index)
print(f"  comment: {c}")
# SKIP tags - not in DLL
print(f"  version: {legacy.ENgetversion()}")
legacy.ENclose()
print("  PASSED")

print("\n=== test_legacy_network_edit ===")
try: legacy.ENclose()
except: pass
legacy.ENinit()
j1 = legacy.ENaddnode("NJ1", EN_JUNCTION)
j2 = legacy.ENaddnode("NJ2", EN_JUNCTION)
t1 = legacy.ENaddnode("T1", EN_TANK)
p1 = legacy.ENaddlink("PL1", EN_PIPE, "NJ1", "NJ2")
legacy.ENsetnodeid(j1, "RENAMED_J1")
assert legacy.ENgetnodeid(j1) == "RENAMED_J1"
legacy.ENsetnodevalue(j1, EN_ELEVATION, 100.0)
legacy.ENsetjuncdata(j2, 50.0, 1.0, "")
legacy.ENsettankdata(t1, 100.0, 5.0, 2.0, 10.0, 20.0, 0.0, "")
legacy.ENsetpipedata(p1, 1000.0, 300.0, 100.0, 0.1)
legacy.ENsetcoord(j1, 10.0, 20.0)
legacy.ENadddemand(j1, 1.0, "", "D1")
num = legacy.ENgetnumdemands(j1)
print(f"  demands: {num}, base={legacy.ENgetbasedemand(j1, num)}")
legacy.ENsetbasedemand(j1, num, 5.0)
legacy.ENdeletedemand(j1, num)
legacy.ENsetvertices(p1, [15.0, 25.0], [25.0, 35.0])
# SKIP ENsetvertex
legacy.ENdeletelink(p1, 1)
legacy.ENdeletenode(j1, 1)
legacy.ENclose()
print("  PASSED")

print("\n=== test_legacy_simulation_stepped ===")
legacy.ENopen(NET1)
legacy.ENsolveH()
legacy.ENsetqualtype(EN_CHEM, "Chlorine", "mg/L", "")
legacy.ENopenQ()
legacy.ENinitQ(0)
tq = legacy.ENrunQ()
tqleft = legacy.ENnextQ()
legacy.ENcloseQ()
legacy.ENclose()
print("  PASSED")

print("\n=== test_legacy_patterns_curves ===")
try: legacy.ENclose()
except: pass
legacy.ENinit()

print("  Adding pattern...")
p_idx = legacy.ENaddpattern("PAT_LEG")
print(f"  p_idx={p_idx}")
legacy.ENsetpattern(p_idx, [1.0, 1.2, 0.8])
assert legacy.ENgetpatternlen(p_idx) == 3
assert legacy.ENgetpatternid(p_idx) == "PAT_LEG"
legacy.ENsetpatternvalue(p_idx, 2, 1.5)
assert legacy.ENgetpatternvalue(p_idx, 2) == 1.5
print("  Deleting pattern...")
legacy.ENdeletepattern(p_idx)

print("  Adding curve...")
c_idx = legacy.ENaddcurve("CURVE_LEG")
print(f"  c_idx={c_idx}")
# SKIP ENsetcurvetype
legacy.ENsetcurvevalue(c_idx, 1, 10.0, 100.0)
x, y = legacy.ENgetcurvevalue(c_idx, 1)
print(f"  curve val: x={x}, y={y}")
assert legacy.ENgetcurvelen(c_idx) == 1
print("  Deleting curve...")
legacy.ENdeletecurve(c_idx)

print("  ENclose...")
legacy.ENclose()
print("  PASSED - NO CRASH!")
