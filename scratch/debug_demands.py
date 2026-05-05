from entoolkit import legacy, constants
import os

def debug_demands():
    try: legacy.ENclose()
    except: pass
    
    legacy.ENinit()
    j1 = legacy.ENaddnode("NJ1", constants.EN_JUNCTION)
    print(f"Added node J1 with index {j1}")
    
    val_to_set = 1.23
    print(f"Adding demand {val_to_set}...")
    legacy.ENadddemand(j1, val_to_set, "", "D1")
    
    num = legacy.ENgetnumdemands(j1)
    print(f"Number of demands: {num}")
    
    for i in range(1, num + 1):
        # Try double
        base_double = legacy.ENgetbasedemand(j1, i)
        print(f"Demand {i} (as double): {base_double}")
        
    legacy.ENclose()

if __name__ == "__main__":
    debug_demands()
