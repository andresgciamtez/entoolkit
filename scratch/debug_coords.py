import ctypes
from entoolkit import legacy, constants

def debug_coords_precision():
    try: legacy.ENclose()
    except: pass
    
    legacy.ENinit()
    lib = legacy._lib
    j1 = legacy.ENaddnode("NJ1", constants.EN_JUNCTION)
    
    x_set, y_set = 1234.56, 7890.12
    print(f"Setting coord ({x_set}, {y_set})...")
    
    # Try as double
    try:
        lib.ENsetcoord(j1, ctypes.c_double(x_set), ctypes.c_double(y_set))
        print("ENsetcoord(double) succeeded")
    except Exception as e:
        print(f"ENsetcoord(double) failed: {e}")
        
    x_val = ctypes.c_double()
    y_val = ctypes.c_double()
    lib.ENgetcoord(j1, ctypes.byref(x_val), ctypes.byref(y_val))
    print(f"Got coord (as double): ({x_val.value}, {y_val.value})")
    
    # Try as float
    x_f = ctypes.c_float()
    y_f = ctypes.c_float()
    lib.ENgetcoord(j1, ctypes.byref(x_f), ctypes.byref(y_f))
    print(f"Got coord (as float): ({x_f.value}, {y_f.value})")
    
    legacy.ENclose()

if __name__ == "__main__":
    debug_coords_precision()
