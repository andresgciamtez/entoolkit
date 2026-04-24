import os
import sys
from entoolkit import legacy, EPANETProject, EN_PRESSURE

def verify_23_features():
    print("--- Verifying EPANET 2.3 Features in EnToolkit ---")
    
    # 1. Check Library Versions
    v_legacy = legacy.ENgetversion()
    print(f"Legacy API Version: {v_legacy}")
    
    proj = EPANETProject()
    try:
        v_toolkit = proj.getversion()
        print(f"Modern API Version: {v_toolkit}")
    except Exception as e:
        print(f"Modern API Version Error: {e}")
    
    # 2. Check Vector API Exports in DLL
    from entoolkit.legacy import _lib
    
    print("\n--- DLL Exports (Legacy) ---")
    for func in ["ENgetnodevalues", "ENgetlinkvalues"]:
        has_it = hasattr(_lib, func)
        print(f"{func}: {'FOUND' if has_it else 'NOT FOUND (Fallback will be used)'}")
        
    print("\n--- DLL Exports (Handle-Based) ---")
    for func in ["EN_getnodevalues", "EN_getlinkvalues", "EN_getversion"]:
        has_it = hasattr(_lib, func)
        print(f"{func}: {'FOUND' if has_it else 'NOT FOUND'}")

    # 3. Functional Test (requires a network)
    net1_path = os.path.join("tests", "networks", "Net1.inp")
    if os.path.exists(net1_path):
        print("\n--- Functional Test (Net1.inp) ---")
        
        # Legacy
        legacy.ENopen(net1_path, "verify_legacy.rpt")
        legacy.ENsolveH()
        pressures_l = legacy.ENgetnodevalues(EN_PRESSURE)
        print(f"Legacy Vector Fetch: Success ({len(pressures_l)} nodes)")
        legacy.ENclose()
        
        # Modern
        proj.open(net1_path, "verify_toolkit.rpt")
        proj.solveH()
        pressures_t = proj.getnodevalues(EN_PRESSURE)
        print(f"Modern Vector Fetch: Success ({len(pressures_t)} nodes)")
        
        # Cross-check first value
        if len(pressures_l) > 0 and len(pressures_t) > 0:
            print(f"Precision Check (Node 1): Legacy={pressures_l[0]:.6f}, Modern={pressures_t[0]:.6f}")
            
        proj.close()
    else:
        print(f"\n[SKIP] Functional test skipped: {net1_path} not found.")

    proj.delete()
    print("\nVerification complete.")

if __name__ == "__main__":
    # Add current dir to path to find entoolkit
    sys.path.insert(0, os.path.abspath("."))
    verify_23_features()
