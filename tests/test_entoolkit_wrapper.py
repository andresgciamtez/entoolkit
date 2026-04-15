import os
import pytest
from entoolkit import toolkit

# Path to Net1.inp
NET1_PATH = os.path.join(os.path.dirname(__file__), "networks", "Net1.inp")

def test_version():
    assert toolkit.ENgetversion() == 20200

def test_simulation():
    # Run full simulation
    toolkit.ENopen(NET1_PATH, "test_toolkit.rpt", "")
    toolkit.ENsolveH()
    
    # Check some values
    # Node 1 is a junction in Net1
    idx = toolkit.ENgetnodeindex("10")
    pressure = toolkit.ENgetnodevalue(idx, toolkit.EN_PRESSURE)
    assert pressure > 0
    
    toolkit.ENclose()
    if os.path.exists("test_toolkit.rpt"):
        os.remove("test_toolkit.rpt")

def test_demand_api():
    toolkit.ENinit("test_demand.rpt", "", toolkit.EN_LPS, toolkit.EN_HW)
    
    idx = toolkit.ENaddnode("D_TEST", toolkit.EN_JUNCTION)
    toolkit.ENadddemand(idx, 15.0, "", "Category_A")
    
    # Net1 node addition usually counts from 1 if empty
    num = toolkit.ENgetnumdemands(idx)
    # Default demand (0) + Category_A
    assert num >= 1
    
    toolkit.ENclose()
    if os.path.exists("test_demand.rpt"):
        os.remove("test_demand.rpt")
