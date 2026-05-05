import unittest.mock as mock
import platform
import importlib
import pytest
import os
import sys

def test_platform_logic_isolated():
    """Test the OS and architecture detection branches in legacy.py in an isolated environment."""
    
    import entoolkit.legacy as legacy
    
    test_cases = [
        ("Linux", "x86_64"),
        ("Linux", "aarch64"),
        # Darwin is excluded because the 2.3 code raises FileNotFoundError
        # when macOS binaries don't exist, even under mock.
    ]
    
    for syst, mach in test_cases:
        with mock.patch("platform.system", return_value=syst), \
             mock.patch("platform.machine", return_value=mach), \
             mock.patch("ctypes.CDLL", return_value=mock.Mock()), \
             mock.patch("ctypes.WinDLL", return_value=mock.Mock()):
            
            # Reload inside the context
            importlib.reload(legacy)
            
            if syst == "Linux":
                assert "linux" in str(legacy._lib_path)

    # Test Darwin separately with Path.exists mocked
    with mock.patch("platform.system", return_value="Darwin"), \
         mock.patch("platform.machine", return_value="arm64"), \
         mock.patch("ctypes.CDLL", return_value=mock.Mock()), \
         mock.patch("ctypes.WinDLL", return_value=mock.Mock()), \
         mock.patch("pathlib.Path.exists", return_value=True):
        importlib.reload(legacy)
        assert "darwin" in str(legacy._lib_path)

    # FINAL RELOAD to restore Windows state for other tests
    # No mocks here = real platform (Windows)
    importlib.reload(legacy)
    legacy._project_open = False
