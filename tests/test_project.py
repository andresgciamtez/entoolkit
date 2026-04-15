import os
import pytest
from entoolkit import EPANETProject, EN_PRESSURE, EN_BASEDEMAND, EN_JUNCTION, EN_LPS, EN_HW

NET1_PATH = os.path.join(os.path.dirname(__file__), "networks", "Net1.inp")

def test_project_simulation():
    p = EPANETProject()
    p.open(NET1_PATH, "test_project.rpt", "")
    p.solveH()
    
    idx = p.getnodeindex("10")
    pressure = p.getnodevalue(idx, EN_PRESSURE)
    assert pressure > 0
    
    p.close()
    if os.path.exists("test_project.rpt"):
        os.remove("test_project.rpt")

def test_project_precision():
    """Test double precision in handle-based API."""
    p = EPANETProject()
    p.init("", "", EN_LPS, EN_HW)
    
    idx = p.addnode("PREC_NODE", EN_JUNCTION)
    # High precision value
    test_val = 1.23456789012345
    p.setnodevalue(idx, EN_BASEDEMAND, test_val)
    
    ret_val = p.getnodevalue(idx, EN_BASEDEMAND)
    assert abs(test_val - ret_val) < 1e-12
    p.delete()

def test_project_array_values():
    """Test efficient array retrieval."""
    p = EPANETProject()
    p.open(NET1_PATH)
    
    pressures = p.getnodevalues(EN_PRESSURE)
    assert len(pressures) == p.getcount(0) # EN_NODECOUNT
    assert all(isinstance(v, float) for v in pressures)
    p.close()
