import ctypes
from entoolkit import legacy, constants

def debug_demands_float_input():
    try: legacy.ENclose()
    except: pass
    
    legacy.ENinit()
    lib = legacy._lib
    j1 = legacy.ENaddnode("NJ1", constants.EN_JUNCTION)
    
    val_to_set = 1.23
    print(f"Setting demand {val_to_set} using ENadddemand (FLOAT)...")
    
    # Try calling ENadddemand with float
    # int ENadddemand(int nodeIndex, float baseDemand, int patternIndex, char *demandName)
    try:
        lib.ENadddemand(j1, ctypes.c_float(val_to_set), 0, b"D1")
        print("Call to ENadddemand succeeded")
    except Exception as e:
        print(f"Call to ENadddemand failed: {e}")
    
    num_ptr = ctypes.c_int()
    lib.ENgetnumdemands(j1, ctypes.byref(num_ptr))
    num = num_ptr.value
    print(f"Number of demands: {num}")
    
    for i in range(1, num + 1):
        val_f = ctypes.c_float()
        lib.ENgetbasedemand(j1, i, ctypes.byref(val_f))
        print(f"Demand {i} (as float): {val_f.value}")
        
    legacy.ENclose()

if __name__ == "__main__":
    debug_demands_float_input()
