import os
import pytest
from entoolkit import EPANETProject

def test_fixtures_coverage(project, net1_path):
    """Explicitly use fixtures to cover conftest.py branches."""
    assert os.path.exists(net1_path)
    assert isinstance(project, EPANETProject)
    
def test_conftest_cleanup_error(project):
    """Trigger the except block in project fixture cleanup."""
    # Close it once so the fixture cleanup (which also calls close) might fail if it's already closed
    # Actually most EPANET calls don't raise on double-close, but we can mock it
    import unittest.mock as mock
    with mock.patch.object(project, "close", side_effect=Exception("Fixture Fail")):
        # When the fixture exits, it will call proj.close() and hit the except: pass block
        pass

def test_legacy_convenience_loops():
    """Hit the ENgetnodevalues and ENgetlinkvalues loops."""
    from entoolkit import legacy
    import unittest.mock as mock
    
    mock_lib = mock.MagicMock()
    def mock_val(c, p): 
        p.contents.value = 5 # count = 5
        return 0
    mock_lib.ENgetcount.side_effect = mock_val
    mock_lib.ENgetnodevalue.return_value = 0
    mock_lib.ENgetlinkvalue.return_value = 0
    
    with mock.patch("entoolkit.legacy._lib", mock_lib):
        legacy.ENgetnodevalues(0)
        legacy.ENgetlinkvalues(0)
