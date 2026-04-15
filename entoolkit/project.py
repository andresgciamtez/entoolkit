import ctypes
from typing import Tuple, List, Optional, Union

from .constants import *
from .toolkit import _lib, ENtoolkitError, ERR_MAX_CHAR, MAX_LABEL_LEN

# Define core project creation/deletion types
# EN_createproject(EN_Project *ph) -> ph is pointer to pointer
_lib.EN_createproject.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
_lib.EN_createproject.restype = ctypes.c_int

# EN_deleteproject(EN_Project ph) -> ph is the pointer itself
# Wait, some builds use EN_Project* for delete to set it to NULL. 
# OWA header says: int DLLEXPORT EN_deleteproject(EN_Project ph);
_lib.EN_deleteproject.argtypes = [ctypes.c_void_p]
_lib.EN_deleteproject.restype = ctypes.c_int

# Define EN_init
_lib.EN_init.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
_lib.EN_init.restype = ctypes.c_int

# Define EN_open
_lib.EN_open.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
_lib.EN_open.restype = ctypes.c_int

# Define EN_addnode
_lib.EN_addnode.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
_lib.EN_addnode.restype = ctypes.c_int

# Define EN_getnodevalue
_lib.EN_getnodevalue.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
_lib.EN_getnodevalue.restype = ctypes.c_int

# Define EN_setnodevalue
_lib.EN_setnodevalue.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_double]
_lib.EN_setnodevalue.restype = ctypes.c_int

class EPANETProject:
    """A thread-safe interface to an EPANET project handle.
    
    This class wraps the EPANET 2.2 handle-based API, allowing multiple
    projects to be managed simultaneously.
    
    Note: The handle-based API (EN_ prefix) uses double precision for 
    numerical values, whereas the legacy API (EN prefix) uses float.
    """
    
    def __init__(self):
        self.ph = ctypes.c_void_p()
        ierr = _lib.EN_createproject(ctypes.byref(self.ph))
        if ierr:
            raise ENtoolkitError(ierr)
            
    def __del__(self):
        # We don't call EN_deleteproject in __del__ because it can cause 
        # issues during interpreter shutdown if _lib is already cleaned up.
        # User should call delete() explicitly or use a context manager.
        pass

    def delete(self):
        """Deletes the project and frees memory."""
        if hasattr(self, 'ph') and self.ph:
            _lib.EN_deleteproject(self.ph)
            self.ph = None

    def _check(self, ierr: int):
        if ierr:
            msg = ctypes.create_string_buffer(ERR_MAX_CHAR)
            _lib.EN_geterror(ierr, msg, ERR_MAX_CHAR)
            err_msg = msg.value.decode()
            raise Exception(f"EPANET Error {ierr}: {err_msg}")

    # --- Project Management ---

    def init(self, rpt_file: str, bin_file: str, units: int, hl: int):
        """Initializes a new project."""
        self._check(_lib.EN_init(self.ph, 
                                 ctypes.c_char_p(rpt_file.encode()),
                                 ctypes.c_char_p(bin_file.encode()),
                                 units, hl))

    def open(self, inp_file: str, rpt_file: str = '', bin_file: str = ''):
        """Opens an EPANET project."""
        self._check(_lib.EN_open(self.ph, 
                                 ctypes.c_char_p(inp_file.encode()),
                                 ctypes.c_char_p(rpt_file.encode()),
                                 ctypes.c_char_p(bin_file.encode())))

    def close(self):
        """Closes the project."""
        self._check(_lib.EN_close(self.ph))

    def solveH(self):
        """Solves hydraulics."""
        self._check(_lib.EN_solveH(self.ph))

    # --- Node Properties (Double Precision) ---

    def getnodeindex(self, node_id: str) -> int:
        index = ctypes.c_int()
        self._check(_lib.EN_getnodeindex(self.ph, ctypes.c_char_p(node_id.encode()), ctypes.byref(index)))
        return index.value

    def getnodeid(self, index: int) -> str:
        id_buffer = ctypes.create_string_buffer(MAX_LABEL_LEN + 1)
        self._check(_lib.EN_getnodeid(self.ph, index, id_buffer))
        return id_buffer.value.decode()

    def getnodevalue(self, index: int, prop: int) -> float:
        val = ctypes.c_double()
        self._check(_lib.EN_getnodevalue(self.ph, index, prop, ctypes.byref(val)))
        return float(val.value)

    def setnodevalue(self, index: int, prop: int, value: float):
        self._check(_lib.EN_setnodevalue(self.ph, index, prop, ctypes.c_double(value)))

    def getnodevalues(self, prop: int) -> List[float]:
        """Retrieves values for a property for all nodes."""
        count = self.getcount(EN_NODECOUNT)
        return [self.getnodevalue(i, prop) for i in range(1, count + 1)]

    def addnode(self, node_id: str, node_type: int) -> int:
        index = ctypes.c_int()
        self._check(_lib.EN_addnode(self.ph, ctypes.c_char_p(node_id.encode()), node_type, ctypes.byref(index)))
        return index.value

    # --- Link Properties (Double Precision) ---

    def getlinkindex(self, link_id: str) -> int:
        index = ctypes.c_int()
        self._check(_lib.EN_getlinkindex(self.ph, ctypes.c_char_p(link_id.encode()), ctypes.byref(index)))
        return index.value

    def getlinkid(self, index: int) -> str:
        id_buffer = ctypes.create_string_buffer(MAX_LABEL_LEN + 1)
        self._check(_lib.EN_getlinkid(self.ph, index, id_buffer))
        return id_buffer.value.decode()

    def getlinkvalue(self, index: int, prop: int) -> float:
        val = ctypes.c_double()
        self._check(_lib.EN_getlinkvalue(self.ph, index, prop, ctypes.byref(val)))
        return float(val.value)

    def setlinkvalue(self, index: int, prop: int, value: float):
        self._check(_lib.EN_setlinkvalue(self.ph, index, prop, ctypes.c_double(value)))

    def getlinkvalues(self, prop: int) -> List[float]:
        """Retrieves values for a property for all links."""
        count = self.getcount(EN_LINKCOUNT)
        return [self.getlinkvalue(i, prop) for i in range(1, count + 1)]

    def getcount(self, obj_type: int) -> int:
        count = ctypes.c_int()
        self._check(_lib.EN_getcount(self.ph, obj_type, ctypes.byref(count)))
        return count.value

    # --- Demand Management (New in 2.2) ---

    def getnumdemands(self, node_index: int) -> int:
        num = ctypes.c_int()
        # Ensure argtypes for demand functions if needed, but usually ctypes handles ints fine
        self._check(_lib.EN_getnumdemands(self.ph, node_index, ctypes.byref(num)))
        return num.value

    def getbasedemand(self, node_index: int, demand_index: int) -> float:
        val = ctypes.c_double()
        self._check(_lib.EN_getbasedemand(self.ph, node_index, demand_index, ctypes.byref(val)))
        return float(val.value)

    def setbasedemand(self, node_index: int, demand_index: int, value: float):
        self._check(_lib.EN_setbasedemand(self.ph, node_index, demand_index, ctypes.c_double(value)))

    def adddemand(self, node_index: int, base_demand: float, pattern_name: str = '', demand_name: str = ''):
        self._check(_lib.EN_adddemand(self.ph, node_index, ctypes.c_double(base_demand),
                                      ctypes.c_char_p(pattern_name.encode()),
                                      ctypes.c_char_p(demand_name.encode())))

    def deletedemand(self, node_index: int, demand_index: int):
        self._check(_lib.EN_deletedemand(self.ph, node_index, demand_index))
