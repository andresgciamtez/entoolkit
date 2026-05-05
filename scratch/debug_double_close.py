"""Test if ENclose after ENopen leaves state corrupted for subsequent ENinit."""
import sys, os
sys.path.insert(0, r"d:\Documentos\Code\apps\entoolkit")

def p(msg):
    print(msg, flush=True)

from entoolkit import legacy

NET1 = os.path.abspath(os.path.join(r"d:\Documentos\Code\apps\entoolkit", "tests", "networks", "Net1.inp"))

p("1. ENopen")
legacy.ENopen(NET1)

p("2. ENclose")
legacy.ENclose()

p("3. try ENclose again (should fail)")
try:
    legacy.ENclose()
    p("   ... no error (unexpected)")
except legacy.ENtoolkitError as e:
    p(f"   ... error {e.ierr}: {e}")
except Exception as e:
    p(f"   ... other error: {e}")

p("4. ENinit")
legacy.ENinit()

p("5. ENclose")
legacy.ENclose()

p("ALL DONE!")
