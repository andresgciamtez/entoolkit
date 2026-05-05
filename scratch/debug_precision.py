import ctypes
from entoolkit import legacy, constants

def debug_demands_precision():
    try: legacy.ENclose()
    except: pass
    
    legacy.ENinit()
    lib = legacy._lib
    j1 = legacy.ENaddnode("NJ1", constants.EN_JUNCTION)
    
    val_to_set = 1.23
    print(f"Setting demand {val_to_set} using ENadddemand...")
    
    # Try calling ENadddemand with double
    # int ENadddemand(int nodeIndex, double baseDemand, int patternIndex, char *demandName)
    lib.ENadddemand(j1, ctypes.c_double(val_to_set), 0, b"D1")
    
    num_ptr = ctypes.c_int()
    lib.ENgetnumdemands(j1, ctypes.byref(num_ptr))
    num = num_ptr.value
    print(f"Number of demands: {num}")
    
    for i in range(1, num + 1):
        # Try as float
        val_f = ctypes.c_float()
        lib.ENgetbasedemand(j1, i, ctypes.byref(val_f))
        print(f"Demand {i} (as float): {val_f.value}")
        
        # Try as double
        val_d = ctypes.c_double()
        lib.ENgetbasedemand(j1, i, ctypes.byref(val_d))
        print(f"Demand {i} (as double): {val_d.value}")
        
    legacy.ENclose()

if __name__ == "__main__":
    debug_demands_precision()
