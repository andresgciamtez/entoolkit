"""
Full audit of epanet2.dll exports vs what legacy.py expects.
Uses a FRESH ctypes load (no argtypes set) to avoid interference.
"""
import ctypes
import subprocess, re

DLL = r"d:\Documentos\Code\apps\entoolkit\entoolkit\epanet\windows-x64\epanet2.dll"

# --- 1. List ALL exported symbols from the DLL ---
print("=" * 70)
print("PHASE 1: DLL Exports via dumpbin")
print("=" * 70)

try:
    result = subprocess.run(
        ["dumpbin", "/exports", DLL],
        capture_output=True, text=True, timeout=10
    )
    # Extract function names
    exports = set()
    for line in result.stdout.splitlines():
        m = re.search(r'\d+\s+[0-9A-Fa-f]+\s+[0-9A-Fa-f]+\s+(\w+)', line)
        if m:
            exports.add(m.group(1))
    
    en_funcs = sorted([f for f in exports if f.startswith("EN")])
    print(f"Found {len(en_funcs)} EN* exports:")
    for f in en_funcs:
        print(f"  {f}")
except FileNotFoundError:
    print("dumpbin not available, using ctypes probing instead")
    exports = set()

# --- 2. Probe all functions that test_legacy_exhaust.py needs ---
print("\n" + "=" * 70)
print("PHASE 2: Probing functions needed by test_legacy_exhaust.py")
print("=" * 70)

needed_funcs = [
    # test_legacy_lifecycle_and_metadata
    "ENopen", "ENclose", "ENsettitle", "ENgettitle",
    "ENgetnodeindex", "ENsetcomment", "ENgetcomment",
    "ENsettag", "ENgettag", "ENgetversion",
    # test_legacy_network_edit
    "ENinit", "ENaddnode", "ENaddlink", "ENsetnodeid", "ENgetnodeid",
    "ENgetnodetype", "ENsetnodevalue", "ENgetnodevalue",
    "ENsetjuncdata", "ENsettankdata", "ENsetpipedata",
    "ENsetcoord", "ENgetcoord",
    "ENadddemand", "ENgetnumdemands", "ENgetbasedemand",
    "ENsetbasedemand", "ENdeletedemand",
    "ENgetlinkindex", "ENgetlinkid", "ENgetlinktype", "ENgetlinknodes",
    "ENsetvertices", "ENgetvertexcount", "ENgetvertex", "ENsetvertex",
    "ENdeletelink", "ENdeletenode",
    # test_legacy_simulation_stepped
    "ENsolveH", "ENsetqualtype", "ENopenQ", "ENinitQ", "ENrunQ",
    "ENnextQ", "ENcloseQ",
    # test_legacy_patterns_curves
    "ENaddpattern", "ENsetpattern", "ENgetpatternlen", "ENgetpatternid",
    "ENsetpatternvalue", "ENgetpatternvalue", "ENdeletepattern",
    "ENaddcurve", "ENsetcurvetype", "ENsetcurvevalue",
    "ENgetcurvevalue", "ENgetcurvelen", "ENdeletecurve",
    "ENgetcurveindex",
    # test_legacy_saving
    "ENsaveinpfile", "ENsaveH", "ENsavehydfile", "ENusehydfile",
    # test_legacy_reporting
    "ENsetstatusreport", "ENresetreport", "ENsetreport",
    "ENwriteline",
    # test_legacy_bulk
    "ENgetcount", "ENgetstatistic", "ENsetdemandmodel",
    "ENgetdemandmodel", "ENsetoption", "ENgetoption",
    "ENgetqualtype", "ENgetflowunits",
    # test_legacy_controls
    "ENaddcontrol", "ENgetcontrol", "ENsetcontrol", "ENdeletecontrol",
]

lib = ctypes.WinDLL(DLL)
present = {}
missing = []
for func in sorted(set(needed_funcs)):
    try:
        getattr(lib, func)
        present[func] = True
    except AttributeError:
        missing.append(func)
        present[func] = False

print(f"\nPresent: {sum(1 for v in present.values() if v)}")
print(f"Missing: {len(missing)}")
if missing:
    print("\nMISSING functions:")
    for f in missing:
        print(f"  [X] {f}")

# --- 3. Test actual argument conventions for demand functions ---
print("\n" + "=" * 70)
print("PHASE 3: Empirical signature testing (demands)")
print("=" * 70)

# Load a fresh copy with NO argtypes
lib2 = ctypes.WinDLL(DLL)

# Init a project
lib2.ENinit(b"", b"", 0, 0)
# Add a junction
idx = ctypes.c_int()
lib2.ENaddnode(b"J1", 0, ctypes.byref(idx))
j1 = idx.value
print(f"Added junction J1 at index {j1}")

# Test ENadddemand with different conventions
# Convention A: (int, double, char*, char*) - what docs say for EN_adddemand (OOP API)
# Convention B: (int, float, char*, char*) - what legacy 2.0 used
# Convention C: (int, double, int, char*)  - what web search suggested
# Convention D: (int, float, int, char*)   - alternative

print("\n--- Test A: ENadddemand(int, double, char*, char*) ---")
lib2.ENinit(b"", b"", 0, 0)
lib2.ENaddnode(b"J1", 0, ctypes.byref(idx))
j1 = idx.value
try:
    ierr = lib2.ENadddemand(j1, ctypes.c_double(5.5), b"", b"DA")
    print(f"  Return code: {ierr}")
    num = ctypes.c_int()
    lib2.ENgetnumdemands(j1, ctypes.byref(num))
    print(f"  Num demands: {num.value}")
    for i in range(1, num.value + 1):
        vf = ctypes.c_float()
        lib2.ENgetbasedemand(j1, i, ctypes.byref(vf))
        print(f"  Demand {i} (float ptr): {vf.value}")
except Exception as e:
    print(f"  Error: {e}")

print("\n--- Test B: ENadddemand(int, float, char*, char*) ---")
lib2.ENinit(b"", b"", 0, 0)
lib2.ENaddnode(b"J1", 0, ctypes.byref(idx))
j1 = idx.value
try:
    ierr = lib2.ENadddemand(j1, ctypes.c_float(5.5), b"", b"DB")
    print(f"  Return code: {ierr}")
    num = ctypes.c_int()
    lib2.ENgetnumdemands(j1, ctypes.byref(num))
    print(f"  Num demands: {num.value}")
    for i in range(1, num.value + 1):
        vf = ctypes.c_float()
        lib2.ENgetbasedemand(j1, i, ctypes.byref(vf))
        print(f"  Demand {i} (float ptr): {vf.value}")
except Exception as e:
    print(f"  Error: {e}")

print("\n--- Test C: ENadddemand(int, double, int, char*) ---")
lib2.ENinit(b"", b"", 0, 0)
lib2.ENaddnode(b"J1", 0, ctypes.byref(idx))
j1 = idx.value
try:
    ierr = lib2.ENadddemand(j1, ctypes.c_double(5.5), ctypes.c_int(0), b"DC")
    print(f"  Return code: {ierr}")
    num = ctypes.c_int()
    lib2.ENgetnumdemands(j1, ctypes.byref(num))
    print(f"  Num demands: {num.value}")
    for i in range(1, num.value + 1):
        vf = ctypes.c_float()
        lib2.ENgetbasedemand(j1, i, ctypes.byref(vf))
        print(f"  Demand {i} (float ptr): {vf.value}")
except Exception as e:
    print(f"  Error: {e}")

print("\n--- Test D: ENadddemand(int, float, int, char*) ---")
lib2.ENinit(b"", b"", 0, 0)
lib2.ENaddnode(b"J1", 0, ctypes.byref(idx))
j1 = idx.value
try:
    ierr = lib2.ENadddemand(j1, ctypes.c_float(5.5), ctypes.c_int(0), b"DD")
    print(f"  Return code: {ierr}")
    num = ctypes.c_int()
    lib2.ENgetnumdemands(j1, ctypes.byref(num))
    print(f"  Num demands: {num.value}")
    for i in range(1, num.value + 1):
        vf = ctypes.c_float()
        lib2.ENgetbasedemand(j1, i, ctypes.byref(vf))
        print(f"  Demand {i} (float ptr): {vf.value}")
except Exception as e:
    print(f"  Error: {e}")

# --- 4. Test ENgetbasedemand output type ---
print("\n" + "=" * 70)
print("PHASE 4: ENgetbasedemand output precision")
print("=" * 70)

# Use the best convention found above  
lib2.ENinit(b"", b"", 0, 0)
lib2.ENaddnode(b"J1", 0, ctypes.byref(idx))
j1 = idx.value
# Set a known value via ENsetnodevalue (EN_BASEDEMAND=1)
lib2.ENsetnodevalue(j1, 1, ctypes.c_float(3.14159))

# Read with float pointer
vf = ctypes.c_float()
lib2.ENgetbasedemand(j1, 1, ctypes.byref(vf))
print(f"ENgetbasedemand as float:  {vf.value}")

# Read with double pointer
vd = ctypes.c_double()
lib2.ENgetbasedemand(j1, 1, ctypes.byref(vd))
print(f"ENgetbasedemand as double: {vd.value}")

# Also read via ENgetnodevalue
vf2 = ctypes.c_float()
lib2.ENgetnodevalue(j1, 1, ctypes.byref(vf2))
print(f"ENgetnodevalue as float:   {vf2.value}")

lib2.ENclose()
print("\nDone.")
