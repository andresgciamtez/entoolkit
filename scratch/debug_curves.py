"""Isolate which curve operation causes the heap corruption."""
import ctypes

DLL = r"d:\Documentos\Code\apps\entoolkit\entoolkit\epanet\windows-x64\epanet2.dll"
lib = ctypes.WinDLL(DLL)

_Pchar = ctypes.c_char_p
_Pint = ctypes.POINTER(ctypes.c_int)
_Pfloat = ctypes.POINTER(ctypes.c_float)

# Set argtypes for the functions we'll use
lib.ENinit.argtypes = [_Pchar, _Pchar, ctypes.c_int, ctypes.c_int]
lib.ENinit.restype = ctypes.c_int
lib.ENclose.argtypes = []
lib.ENclose.restype = ctypes.c_int
lib.ENaddcurve.argtypes = [_Pchar]
lib.ENaddcurve.restype = ctypes.c_int
lib.ENgetcurveindex.argtypes = [_Pchar, _Pint]
lib.ENgetcurveindex.restype = ctypes.c_int
lib.ENsetcurvevalue.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float]
lib.ENsetcurvevalue.restype = ctypes.c_int
lib.ENgetcurvevalue.argtypes = [ctypes.c_int, ctypes.c_int, _Pfloat, _Pfloat]
lib.ENgetcurvevalue.restype = ctypes.c_int
lib.ENgetcurvelen.argtypes = [ctypes.c_int, _Pint]
lib.ENgetcurvelen.restype = ctypes.c_int
lib.ENdeletecurve.argtypes = [ctypes.c_int]
lib.ENdeletecurve.restype = ctypes.c_int

print("Step 1: ENinit...")
ierr = lib.ENinit(b"", b"", 0, 0)
print(f"  ierr={ierr}")

print("Step 2: ENaddcurve...")
ierr = lib.ENaddcurve(b"CURVE_TEST")
print(f"  ierr={ierr}")

print("Step 3: ENgetcurveindex...")
idx = ctypes.c_int()
ierr = lib.ENgetcurveindex(b"CURVE_TEST", ctypes.byref(idx))
print(f"  ierr={ierr}, index={idx.value}")

c_idx = idx.value

print("Step 4: ENsetcurvevalue...")
ierr = lib.ENsetcurvevalue(c_idx, 1, ctypes.c_float(10.0), ctypes.c_float(100.0))
print(f"  ierr={ierr}")

print("Step 5: ENgetcurvevalue...")
x = ctypes.c_float()
y = ctypes.c_float()
ierr = lib.ENgetcurvevalue(c_idx, 1, ctypes.byref(x), ctypes.byref(y))
print(f"  ierr={ierr}, x={x.value}, y={y.value}")

print("Step 6: ENgetcurvelen...")
clen = ctypes.c_int()
ierr = lib.ENgetcurvelen(c_idx, ctypes.byref(clen))
print(f"  ierr={ierr}, len={clen.value}")

print("Step 7: ENdeletecurve...")
ierr = lib.ENdeletecurve(c_idx)
print(f"  ierr={ierr}")

print("Step 8: ENclose...")
ierr = lib.ENclose()
print(f"  ierr={ierr}")

print("ALL DONE - no crash!")
