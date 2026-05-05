"""Narrow down crash in network edit."""
import sys, os
sys.path.insert(0, r"d:\Documentos\Code\apps\entoolkit")

def p(msg):
    print(msg, flush=True)

from entoolkit import legacy
from entoolkit import EN_JUNCTION, EN_PIPE, EN_ELEVATION, EN_TANK

NET1 = os.path.abspath(os.path.join(r"d:\Documentos\Code\apps\entoolkit", "tests", "networks", "Net1.inp"))

# Test 1 first
p("=== TEST 1 ===")
try: legacy.ENclose()
except: pass
legacy.ENopen(NET1)
legacy.ENsettitle("L1", "L2", "L3")
legacy.ENgettitle()
index = legacy.ENgetnodeindex("10")
legacy.ENsetcomment(0, index, "Comment")
legacy.ENgetcomment(0, index)
legacy.ENgetversion()
legacy.ENclose()
p("  OK")

# Test 2 step by step
p("=== TEST 2 ===")
try: legacy.ENclose()
except: pass

p("  2.1: ENinit")
legacy.ENinit()

p("  2.2: ENaddnode NJ1")
j1 = legacy.ENaddnode("NJ1", EN_JUNCTION)

p("  2.3: ENaddnode NJ2")
j2 = legacy.ENaddnode("NJ2", EN_JUNCTION)

p("  2.4: ENaddnode T1")
t1 = legacy.ENaddnode("T1", EN_TANK)

p("  2.5: ENaddlink PL1")
p1 = legacy.ENaddlink("PL1", EN_PIPE, "NJ1", "NJ2")

p("  2.6: ENsetnodeid")
legacy.ENsetnodeid(j1, "R_J1")

p("  2.7: ENsetnodevalue")
legacy.ENsetnodevalue(j1, EN_ELEVATION, 100.0)

p("  2.8: ENsetjuncdata")
legacy.ENsetjuncdata(j2, 50.0, 1.0, "")

p("  2.9: ENsettankdata")
legacy.ENsettankdata(t1, 100.0, 5.0, 2.0, 10.0, 20.0, 0.0, "")

p("  2.10: ENsetpipedata")
legacy.ENsetpipedata(p1, 1000.0, 300.0, 100.0, 0.1)

p("  2.11: ENsetcoord")
legacy.ENsetcoord(j1, 10.0, 20.0)

p("  2.12: ENadddemand")
legacy.ENadddemand(j1, 1.0, "", "D1")

p("  2.13: ENgetnumdemands")
num = legacy.ENgetnumdemands(j1)
p(f"        num={num}")

p("  2.14: ENgetbasedemand")
bd = legacy.ENgetbasedemand(j1, num)
p(f"        base={bd}")

p("  2.15: ENsetbasedemand")
legacy.ENsetbasedemand(j1, num, 5.0)

p("  2.16: ENdeletedemand")
legacy.ENdeletedemand(j1, num)

p("  2.17: ENsetvertices")
legacy.ENsetvertices(p1, [15.0, 25.0], [25.0, 35.0])

p("  2.18: ENdeletelink")
legacy.ENdeletelink(p1, 1)

p("  2.19: ENdeletenode")
legacy.ENdeletenode(j1, 1)

p("  2.20: ENclose")
legacy.ENclose()

p("  OK!")
