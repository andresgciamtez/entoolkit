"""Reproduce the exact test_legacy_patterns_curves sequence."""
import ctypes

DLL = r"d:\Documentos\Code\apps\entoolkit\entoolkit\epanet\windows-x64\epanet2.dll"
lib = ctypes.WinDLL(DLL)

_Pchar = ctypes.c_char_p
_Pint = ctypes.POINTER(ctypes.c_int)
_Pfloat = ctypes.POINTER(ctypes.c_float)

# Set minimal argtypes
fns = {
    "ENinit": [_Pchar, _Pchar, ctypes.c_int, ctypes.c_int],
    "ENclose": [],
    "ENaddpattern": [_Pchar],
    "ENgetpatternindex": [_Pchar, _Pint],
    "ENsetpattern": [ctypes.c_int, _Pfloat, ctypes.c_int],
    "ENgetpatternlen": [ctypes.c_int, _Pint],
    "ENgetpatternid": [ctypes.c_int, _Pchar],
    "ENsetpatternvalue": [ctypes.c_int, ctypes.c_int, ctypes.c_float],
    "ENgetpatternvalue": [ctypes.c_int, ctypes.c_int, _Pfloat],
    "ENdeletepattern": [ctypes.c_int],
    "ENaddcurve": [_Pchar],
    "ENgetcurveindex": [_Pchar, _Pint],
    "ENsetcurvevalue": [ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float],
    "ENgetcurvevalue": [ctypes.c_int, ctypes.c_int, _Pfloat, _Pfloat],
    "ENgetcurvelen": [ctypes.c_int, _Pint],
    "ENdeletecurve": [ctypes.c_int],
}
for name, args in fns.items():
    f = getattr(lib, name)
    f.argtypes = args
    f.restype = ctypes.c_int

print("1. ENinit")
lib.ENinit(b"", b"", 0, 0)

print("2. ENaddpattern")
lib.ENaddpattern(b"PAT_LEG")

print("3. ENgetpatternindex")
idx = ctypes.c_int()
lib.ENgetpatternindex(b"PAT_LEG", ctypes.byref(idx))
p_idx = idx.value
print(f"   p_idx={p_idx}")

print("4. ENsetpattern")
factors = [1.0, 1.2, 0.8]
cfactors = (ctypes.c_float * 3)(*factors)
lib.ENsetpattern(p_idx, cfactors, 3)

print("5. ENgetpatternlen")
plen = ctypes.c_int()
lib.ENgetpatternlen(p_idx, ctypes.byref(plen))
print(f"   len={plen.value}")

print("6. ENgetpatternid")
pid = ctypes.create_string_buffer(32)
lib.ENgetpatternid(p_idx, pid)
print(f"   id={pid.value.decode()}")

print("7. ENsetpatternvalue")
lib.ENsetpatternvalue(p_idx, 2, ctypes.c_float(1.5))

print("8. ENgetpatternvalue")
pval = ctypes.c_float()
lib.ENgetpatternvalue(p_idx, 2, ctypes.byref(pval))
print(f"   val={pval.value}")

print("9. ENdeletepattern")
ierr = lib.ENdeletepattern(p_idx)
print(f"   ierr={ierr}")

print("10. ENaddcurve")
ierr = lib.ENaddcurve(b"CURVE_LEG")
print(f"   ierr={ierr}")

print("11. ENgetcurveindex")
cidx = ctypes.c_int()
lib.ENgetcurveindex(b"CURVE_LEG", ctypes.byref(cidx))
c_idx = cidx.value
print(f"   c_idx={c_idx}")

# SKIP ENsetcurvetype - not in DLL

print("12. ENsetcurvevalue")
ierr = lib.ENsetcurvevalue(c_idx, 1, ctypes.c_float(10.0), ctypes.c_float(100.0))
print(f"   ierr={ierr}")

print("13. ENgetcurvevalue")
x = ctypes.c_float()
y = ctypes.c_float()
ierr = lib.ENgetcurvevalue(c_idx, 1, ctypes.byref(x), ctypes.byref(y))
print(f"   ierr={ierr}, x={x.value}, y={y.value}")

print("14. ENgetcurvelen")
clen = ctypes.c_int()
ierr = lib.ENgetcurvelen(c_idx, ctypes.byref(clen))
print(f"   ierr={ierr}, len={clen.value}")

print("15. ENdeletecurve")
ierr = lib.ENdeletecurve(c_idx)
print(f"   ierr={ierr}")

print("16. ENclose")
ierr = lib.ENclose()
print(f"   ierr={ierr}")

print("ALL DONE - no crash!")
