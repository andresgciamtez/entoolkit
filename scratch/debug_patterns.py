import ctypes
from entoolkit import legacy, constants

def debug_patterns_precision():
    try: legacy.ENclose()
    except: pass
    
    legacy.ENinit()
    lib = legacy._lib
    
    pat_idx = legacy.ENaddpattern("PAT1")
    factors = [1.0, 1.5, 0.5]
    print(f"Setting pattern factors {factors}...")
    
    # Try as float
    cfactors_f = (ctypes.c_float * len(factors))(*factors)
    lib.ENsetpattern(pat_idx, cfactors_f, len(factors))
    
    val_f = ctypes.c_float()
    lib.ENgetpatternvalue(pat_idx, 2, ctypes.byref(val_f))
    print(f"Pattern value 2 (as float): {val_f.value}")
    
    legacy.ENclose()

if __name__ == "__main__":
    debug_patterns_precision()
