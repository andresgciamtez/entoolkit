import ctypes
import os

lib_path = r"d:\Documentos\Code\apps\entoolkit\entoolkit\epanet\windows-x64\epanet2.dll"
try:
    lib = ctypes.WinDLL(lib_path)
    print(f"Library loaded from {lib_path}")
    
    funcs = ["ENsettag", "ENgettag", "ENsetcomment", "ENgetcomment", "ENadddemand", "ENgetbasedemand", "ENclose"]
    for func in funcs:
        try:
            getattr(lib, func)
            print(f"Found: {func}")
        except AttributeError:
            print(f"MISSING: {func}")
            
    # Check version
    try:
        version_ptr = ctypes.c_int()
        lib.ENgetversion(ctypes.byref(version_ptr))
        print(f"Version: {version_ptr.value}")
    except Exception as e:
        print(f"Error getting version: {e}")
        
except Exception as e:
    print(f"Error loading library: {e}")
