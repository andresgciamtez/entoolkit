import unittest
import os
import threading
from entoolkit import legacy, EPANETProject, constants

NET1_PATH = os.path.join(os.path.dirname(__file__), "tests", "networks", "Net1.inp")

class TestEntoolkit(unittest.TestCase):
    
    def test_01_version(self):
        self.assertGreaterEqual(legacy.ENgetversion(), 20200)

    def test_02_legacy_sim(self):
        legacy.ENopen(NET1_PATH, "test_legacy.rpt", "")
        legacy.ENsolveH()
        idx = legacy.ENgetnodeindex("10")
        pressure = legacy.ENgetnodevalue(idx, constants.EN_PRESSURE)
        self.assertGreater(pressure, 0)
        legacy.ENclose()
        if os.path.exists("test_legacy.rpt"): os.remove("test_legacy.rpt")

    def test_03_project_precision(self):
        p = EPANETProject()
        p.init("", "", constants.EN_LPS, constants.EN_HW)
        idx = p.addnode("PREC_NODE", constants.EN_JUNCTION)
        test_val = 1.23456789012345
        p.setnodevalue(idx, constants.EN_BASEDEMAND, test_val)
        ret_val = p.getnodevalue(idx, constants.EN_BASEDEMAND)
        self.assertLess(abs(test_val - ret_val), 1e-12)
        p.delete()

    def test_04_project_concurrency(self):
        results = {}
        def run_sim(tid):
            try:
                p = EPANETProject()
                p.open(NET1_PATH, f"thread_{tid}.rpt")
                p.solveH()
                results[tid] = p.getnodevalue(p.getnodeindex("10"), constants.EN_PRESSURE)
                p.close()
                if os.path.exists(f"thread_{tid}.rpt"): os.remove(f"thread_{tid}.rpt")
            except Exception as e:
                results[tid] = e

        t1 = threading.Thread(target=run_sim, args=(1,))
        t2 = threading.Thread(target=run_sim, args=(2,))
        t1.start(); t2.start()
        t1.join(); t2.join()
        
        self.assertGreater(results[1], 0)
        self.assertEqual(results[1], results[2])

if __name__ == '__main__':
    unittest.main()
