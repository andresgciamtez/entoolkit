import ctypes
import platform
import sys
from pathlib import Path
from typing import Tuple, List, Optional, Callable, Union

from .constants import *

# --- Library Loading ---

_OS_NAME = platform.system().lower()
_MACHINE = platform.machine().lower()
_BASE_PATH = Path(__file__).parent / "epanet"

# Architecture detection (x64, x86, arm64)
if "arm" in _MACHINE or "aarch64" in _MACHINE:
    _arch = "arm64" 
elif "64" in _MACHINE:
    _arch = "x64"
else:
    _arch = "x86"

# Library selection based on platform
if _OS_NAME == "windows":
    _lib_path = _BASE_PATH / f"windows-{_arch}" / "epanet2.dll"
    # Using WinDLL for __stdcall convention on Windows
    _lib = ctypes.WinDLL(str(_lib_path))
elif _OS_NAME == "darwin":
    _lib_path = _BASE_PATH / f"darwin-{_arch}" / "libepanet.dylib"
    _lib = ctypes.CDLL(str(_lib_path))
else: # Linux
    _lib_path = _BASE_PATH / f"linux-{_arch}" / "libepanet.so"
    _lib = ctypes.CDLL(str(_lib_path))

# --- General Constants ---

MAX_LABEL_LEN = 15
ERR_MAX_CHAR = 80


def ENinit(rpt_file: str, bin_file: str, units_type: int, headloss_type: int) -> None:
    """Initializes the toolkit with a new project."""
    ierr = _lib.ENinit(ctypes.c_char_p(rpt_file.encode()),
                       ctypes.c_char_p(bin_file.encode()),
                       units_type, headloss_type)
    if ierr:
        raise ENtoolkitError(ierr)


def ENgettitle() -> Tuple[str, str, str]:
    """Gets the project title lines."""
    l1 = ctypes.create_string_buffer(EN_MAXMSG + 1)
    l2 = ctypes.create_string_buffer(EN_MAXMSG + 1)
    l3 = ctypes.create_string_buffer(EN_MAXMSG + 1)
    ierr = _lib.ENgettitle(l1, l2, l3)
    if ierr:
        raise ENtoolkitError(ierr)
    return l1.value.decode(), l2.value.decode(), l3.value.decode()


def ENsettitle(line1: str, line2: str, line3: str) -> None:
    """Sets the project title lines."""
    ierr = _lib.ENsettitle(ctypes.c_char_p(line1.encode()),
                           ctypes.c_char_p(line2.encode()),
                           ctypes.c_char_p(line3.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetcomment(obj_type: int, index: int) -> str:
    """Gets the description comment for a network object."""
    comment = ctypes.create_string_buffer(EN_MAXMSG + 1)
    ierr = _lib.ENgetcomment(obj_type, index, comment)
    if ierr:
        raise ENtoolkitError(ierr)
    return comment.value.decode()


def ENsetcomment(obj_type: int, index: int, comment: str) -> None:
    """Sets the description comment for a network object."""
    ierr = _lib.ENsetcomment(obj_type, index, ctypes.c_char_p(comment.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENgettag(obj_type: int, index: int) -> str:
    """Gets the tag string for a network object."""
    tag = ctypes.create_string_buffer(EN_MAXMSG + 1)
    ierr = _lib.ENgettag(obj_type, index, tag)
    if ierr:
        raise ENtoolkitError(ierr)
    return tag.value.decode()


def ENsettag(obj_type: int, index: int, tag: str) -> None:
    """Sets the tag string for a network object."""
    ierr = _lib.ENsettag(obj_type, index, ctypes.c_char_p(tag.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENgeterror(error_code: int) -> str:
    """Converts a toolkit error code to a readable message string."""
    error_msg = ctypes.create_string_buffer(ERR_MAX_CHAR)
    _lib.ENgeterror(error_code, ctypes.byref(error_msg), ERR_MAX_CHAR)
    return error_msg.value.decode()


class ENtoolkitError(Exception):
    """Exception raised for errors in the EPANET Toolkit.

    Attributes:
        ierr (int): The error code returned by the toolkit.
        warning (bool): True if the code represents a warning (< 100).
        message (str): Descriptive error message.
    """

    def __init__(self, ierr: int):
        self.ierr = ierr
        self.warning = ierr < 100
        self.message = ENgeterror(ierr)
        if not self.message and ierr:
            self.message = f"ENtoolkit Undocumented Error {ierr}: check EPANET documentation/headers"

    def __str__(self) -> str:
        return self.message


def ENepanet(inp_file: str, rpt_file: str = '', bin_file: str = '',
             vfunc: Optional[Callable[[str], None]] = None) -> None:
    """Runs a complete EPANET simulation.

    Args:
        inp_file: Path to the input file (.inp).
        rpt_file: Path to the report file (.rpt).
        bin_file: Path to the optional binary output file.
        vfunc: Optional callback function that accepts a status string.
    """
    callback = None
    if vfunc is not None:
        cfunc = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
        callback = cfunc(lambda msg: vfunc(msg.decode()))

    ierr = _lib.ENepanet(ctypes.c_char_p(inp_file.encode()),
                         ctypes.c_char_p(rpt_file.encode()),
                         ctypes.c_char_p(bin_file.encode()),
                         callback)
    if ierr:
        raise ENtoolkitError(ierr)


def ENopen(inp_file: str, rpt_file: str = '', bin_file: str = '') -> None:
    """Opens an EPANET project for analysis."""
    ierr = _lib.ENopen(ctypes.c_char_p(inp_file.encode()),
                       ctypes.c_char_p(rpt_file.encode()),
                       ctypes.c_char_p(bin_file.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENclose() -> None:
    """Closes the EPANET toolkit and releases files."""
    ierr = _lib.ENclose()
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetnodeindex(node_id: str) -> int:
    """Gets the index of a node from its ID string."""
    index_ptr = ctypes.c_int()
    ierr = _lib.ENgetnodeindex(ctypes.c_char_p(node_id.encode()), ctypes.byref(index_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return index_ptr.value


def ENgetnodeid(index: int) -> str:
    """Gets the ID string of a node from its index."""
    id_buffer = ctypes.create_string_buffer(MAX_LABEL_LEN + 1)
    ierr = _lib.ENgetnodeid(index, ctypes.byref(id_buffer))
    if ierr:
        raise ENtoolkitError(ierr)
    return id_buffer.value.decode()


def ENgetnodetype(index: int) -> int:
    """Gets the type code for a node."""
    type_ptr = ctypes.c_int()
    ierr = _lib.ENgetnodetype(index, ctypes.byref(type_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return type_ptr.value


def ENgetnodevalue(index: int, param_code: int) -> float:
    """Gets the value of a specific node parameter."""
    value_ptr = ctypes.c_float()
    ierr = _lib.ENgetnodevalue(index, param_code, ctypes.byref(value_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return float(value_ptr.value)


def ENaddnode(node_id: str, node_type: int) -> int:
    """Adds a new node to the network."""
    index_ptr = ctypes.c_int()
    ierr = _lib.ENaddnode(ctypes.c_char_p(node_id.encode()), node_type, ctypes.byref(index_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return index_ptr.value


def ENdeletenode(index: int, action_code: int) -> None:
    """Deletes a node from the network."""
    ierr = _lib.ENdeletenode(index, action_code)
    if ierr:
        raise ENtoolkitError(ierr)


def ENsetnodeid(index: int, new_id: str) -> None:
    """Changes the ID for a node."""
    ierr = _lib.ENsetnodeid(index, ctypes.c_char_p(new_id.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENadddemand(node_index: int, base_demand: float, pattern_name: str = '', demand_name: str = '') -> None:
    """Appends a new demand to a junction node demands list."""
    ierr = _lib.ENadddemand(node_index, ctypes.c_double(base_demand),
                            ctypes.c_char_p(pattern_name.encode()),
                            ctypes.c_char_p(demand_name.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENdeletedemand(node_index: int, demand_index: int) -> None:
    """Deletes a demand from a junction node."""
    ierr = _lib.ENdeletedemand(node_index, demand_index)
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetnumdemands(node_index: int) -> int:
    """Retrieves the number of demand categories for a junction node."""
    num_demands = ctypes.c_int()
    ierr = _lib.ENgetnumdemands(node_index, ctypes.byref(num_demands))
    if ierr:
        raise ENtoolkitError(ierr)
    return num_demands.value


def ENgetbasedemand(node_index: int, demand_index: int) -> float:
    """Gets the base demand for one of a node's demand categories."""
    base_demand = ctypes.c_double()
    ierr = _lib.ENgetbasedemand(node_index, demand_index, ctypes.byref(base_demand))
    if ierr:
        raise ENtoolkitError(ierr)
    return float(base_demand.value)


def ENsetbasedemand(node_index: int, demand_index: int, base_demand: float) -> None:
    """Sets the base demand for one of a node's demand categories."""
    ierr = _lib.ENsetbasedemand(node_index, demand_index, ctypes.c_double(base_demand))
    if ierr:
        raise ENtoolkitError(ierr)


def ENsetjuncdata(index: int, elevation: float, demand: float, pattern_id: str) -> None:
    """Sets junctions parameters."""
    ierr = _lib.ENsetjuncdata(index, ctypes.c_float(elevation),
                              ctypes.c_float(demand),
                              ctypes.c_char_p(pattern_id.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENsettankdata(index: int, elevation: float, init_level: float, min_level: float,
                  max_level: float, diameter: float, min_vol: float, vol_curve: str) -> None:
    """Sets tank parameters."""
    ierr = _lib.ENsettankdata(index, ctypes.c_float(elevation),
                              ctypes.c_float(init_level), ctypes.c_float(min_level),
                              ctypes.c_float(max_level), ctypes.c_float(diameter),
                              ctypes.c_float(min_vol), ctypes.c_char_p(vol_curve.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetcoord(index: int) -> Tuple[float, float]:
    """Gets the X, Y coordinates for a node."""
    x = ctypes.c_double()
    y = ctypes.c_double()
    ierr = _lib.ENgetcoord(index, ctypes.byref(x), ctypes.byref(y))
    if ierr:
        raise ENtoolkitError(ierr)
    return x.value, y.value


def ENsetcoord(index: int, x: float, y: float) -> None:
    """Sets the X, Y coordinates for a node."""
    ierr = _lib.ENsetcoord(index, ctypes.c_double(x), ctypes.c_double(y))
    if ierr:
        raise ENtoolkitError(ierr)


def ENsetnodevalue(index: int, param_code: int, value: float) -> None:
    """Sets the value of a specific node parameter."""
    ierr = _lib.ENsetnodevalue(index, param_code, ctypes.c_float(value))
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetlinkindex(link_id: str) -> int:
    """Gets the index of a link from its ID string."""
    index_ptr = ctypes.c_int()
    ierr = _lib.ENgetlinkindex(ctypes.c_char_p(link_id.encode()), ctypes.byref(index_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return index_ptr.value


def ENgetlinkid(index: int) -> str:
    """Gets the ID string of a link from its index."""
    id_buffer = ctypes.create_string_buffer(MAX_LABEL_LEN + 1)
    ierr = _lib.ENgetlinkid(index, ctypes.byref(id_buffer))
    if ierr:
        raise ENtoolkitError(ierr)
    return id_buffer.value.decode()


def ENgetlinktype(index: int) -> int:
    """Gets the type code for a link."""
    type_ptr = ctypes.c_int()
    ierr = _lib.ENgetlinktype(index, ctypes.byref(type_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return type_ptr.value


def ENgetlinknodes(index: int) -> Tuple[int, int]:
    """Gets the indexes of the start and end nodes of a link."""
    from_node_ptr = ctypes.c_int()
    to_node_ptr = ctypes.c_int()
    ierr = _lib.ENgetlinknodes(index, ctypes.byref(from_node_ptr), ctypes.byref(to_node_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return from_node_ptr.value, to_node_ptr.value


def ENgetlinkvalue(index: int, param_code: int) -> float:
    """Gets the value of a specific link parameter."""
    value_ptr = ctypes.c_float()
    ierr = _lib.ENgetlinkvalue(index, param_code, ctypes.byref(value_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return float(value_ptr.value)


def ENaddlink(link_id: str, link_type: int, from_node: str, to_node: str) -> int:
    """Adds a new link to the network."""
    index_ptr = ctypes.c_int()
    ierr = _lib.ENaddlink(ctypes.c_char_p(link_id.encode()), link_type,
                          ctypes.c_char_p(from_node.encode()),
                          ctypes.c_char_p(to_node.encode()),
                          ctypes.byref(index_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return index_ptr.value


def ENdeletelink(index: int, action_code: int) -> None:
    """Deletes a link from the network."""
    ierr = _lib.ENdeletelink(index, action_code)
    if ierr:
        raise ENtoolkitError(ierr)


def ENsetpipedata(index: int, length: float, diameter: float, roughness: float, mloss: float) -> None:
    """Sets pipe parameters."""
    ierr = _lib.ENsetpipedata(index, ctypes.c_float(length), ctypes.c_float(diameter),
                              ctypes.c_float(roughness), ctypes.c_float(mloss))
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetvertexcount(index: int) -> int:
    """Gets the number of vertices for a link."""
    count_ptr = ctypes.c_int()
    ierr = _lib.ENgetvertexcount(index, ctypes.byref(count_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return count_ptr.value


def ENgetvertex(index: int, vertex: int) -> Tuple[float, float]:
    """Gets the X, Y coordinates for a link vertex."""
    x = ctypes.c_double()
    y = ctypes.c_double()
    ierr = _lib.ENgetvertex(index, vertex, ctypes.byref(x), ctypes.byref(y))
    if ierr:
        raise ENtoolkitError(ierr)
    return x.value, y.value


def ENsetvertex(index: int, vertex: int, x: float, y: float) -> None:
    """Sets the X, Y coordinates for a link vertex."""
    ierr = _lib.ENsetvertex(index, vertex, ctypes.c_double(x), ctypes.c_double(y))
    if ierr:
        raise ENtoolkitError(ierr)


def ENsetvertices(index: int, x: List[float], y: List[float]) -> None:
    """Sets all vertices for a link."""
    count = len(x)
    cx = (ctypes.c_double * count)(*x)
    cy = (ctypes.c_double * count)(*y)
    ierr = _lib.ENsetvertices(index, cx, cy, count)
    if ierr:
        raise ENtoolkitError(ierr)


def ENsetlinkvalue(index: int, param_code: int, value: float) -> None:
    """Sets the value of a specific link parameter."""
    ierr = _lib.ENsetlinkvalue(index, param_code, ctypes.c_float(value))
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetpatternid(index: int) -> str:
    """Gets the ID string of a time pattern."""
    id_buffer = ctypes.create_string_buffer(MAX_LABEL_LEN + 1)
    ierr = _lib.ENgetpatternid(index, ctypes.byref(id_buffer))
    if ierr:
        raise ENtoolkitError(ierr)
    return id_buffer.value.decode()


def ENgetpatternindex(pattern_id: str) -> int:
    """Gets the index of a time pattern from its ID."""
    index_ptr = ctypes.c_int()
    ierr = _lib.ENgetpatternindex(ctypes.c_char_p(pattern_id.encode()), ctypes.byref(index_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return index_ptr.value


def ENgetpatternlen(index: int) -> int:
    """Gets the number of periods in a time pattern."""
    len_ptr = ctypes.c_int()
    ierr = _lib.ENgetpatternlen(index, ctypes.byref(len_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return len_ptr.value


def ENgetpatternvalue(index: int, period: int) -> float:
    """Gets the multiplier for a specific pattern period."""
    value_ptr = ctypes.c_float()
    ierr = _lib.ENgetpatternvalue(index, period, ctypes.byref(value_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return float(value_ptr.value)


def ENaddpattern(pattern_id: str) -> int:
    """Adds a new time pattern to the network."""
    index_ptr = ctypes.c_int()
    ierr = _lib.ENaddpattern(ctypes.c_char_p(pattern_id.encode()), ctypes.byref(index_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return index_ptr.value


def ENdeletepattern(index: int) -> None:
    """Deletes a time pattern from the network."""
    ierr = _lib.ENdeletepattern(index)
    if ierr:
        raise ENtoolkitError(ierr)


def ENsetpattern(index: int, factors: List[float]) -> None:
    """Sets all multipliers for a specific pattern."""
    num_factors = len(factors)
    cfactors = (ctypes.c_float * num_factors)(*factors)
    ierr = _lib.ENsetpattern(index, cfactors, num_factors)
    if ierr:
        raise ENtoolkitError(ierr)


def ENsetpatternvalue(index: int, period: int, value: float) -> None:
    """Sets the multiplier for a specific pattern period."""
    ierr = _lib.ENsetpatternvalue(index, period, ctypes.c_float(value))
    if ierr:
        raise ENtoolkitError(ierr)


def ENaddcurve(curve_id: str) -> int:
    """Adds a new data curve to the network."""
    index_ptr = ctypes.c_int()
    ierr = _lib.ENaddcurve(ctypes.c_char_p(curve_id.encode()), ctypes.byref(index_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return index_ptr.value


def ENdeletecurve(index: int) -> None:
    """Deletes a data curve from the network."""
    ierr = _lib.ENdeletecurve(index)
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetcurveindex(curve_id: str) -> int:
    """Gets the index of a data curve from its ID."""
    index_ptr = ctypes.c_int()
    ierr = _lib.ENgetcurveindex(ctypes.c_char_p(curve_id.encode()), ctypes.byref(index_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return index_ptr.value


def ENgetcurveid(index: int) -> str:
    """Gets the ID for a data curve from its index."""
    id_buffer = ctypes.create_string_buffer(MAX_LABEL_LEN + 1)
    ierr = _lib.ENgetcurveid(index, ctypes.byref(id_buffer))
    if ierr:
        raise ENtoolkitError(ierr)
    return id_buffer.value.decode()


def ENgetcurvelen(index: int) -> int:
    """Gets the number of points in a data curve."""
    len_ptr = ctypes.c_int()
    ierr = _lib.ENgetcurvelen(index, ctypes.byref(len_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return len_ptr.value


def ENgetcurvetype(index: int) -> int:
    """Gets the type of a data curve."""
    type_ptr = ctypes.c_int()
    ierr = _lib.ENgetcurvetype(index, ctypes.byref(type_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return type_ptr.value


def ENsetcurvetype(index: int, type_code: int) -> None:
    """Sets the type of a data curve."""
    ierr = _lib.ENsetcurvetype(index, type_code)
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetcurvevalue(index: int, point_index: int) -> Tuple[float, float]:
    """Gets the X and Y values for a point in a data curve."""
    x = ctypes.c_float()
    y = ctypes.c_float()
    ierr = _lib.ENgetcurvevalue(index, point_index, ctypes.byref(x), ctypes.byref(y))
    if ierr:
        raise ENtoolkitError(ierr)
    return float(x.value), float(y.value)


def ENsetcurvevalue(index: int, point_index: int, x: float, y: float) -> None:
    """Sets the X and Y values for a point in a data curve."""
    ierr = _lib.ENsetcurvevalue(index, point_index, ctypes.c_float(x), ctypes.c_float(y))
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetcount(count_code: int) -> int:
    """Gets the number of components of a certain type."""
    count_ptr = ctypes.c_int()
    ierr = _lib.ENgetcount(count_code, ctypes.byref(count_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return count_ptr.value


def ENgetflowunits() -> int:
    """Gets the flow units code for the project."""
    units_ptr = ctypes.c_int()
    ierr = _lib.ENgetflowunits(ctypes.byref(units_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return units_ptr.value


def ENgettimeparam(param_code: int) -> int:
    """Gets the value of a specific time parameter."""
    time_ptr = ctypes.c_int()
    ierr = _lib.ENgettimeparam(param_code, ctypes.byref(time_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return time_ptr.value


def ENsettimeparam(param_code: int, time_value: int) -> None:
    """Sets the value of a specific time parameter."""
    ierr = _lib.ENsettimeparam(param_code, time_value)
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetqualtype() -> Tuple[int, int]:
    """Gets the type of water quality analysis and trace node."""
    q_ptr = ctypes.c_int()
    t_ptr = ctypes.c_int()
    ierr = _lib.ENgetqualtype(ctypes.byref(q_ptr), ctypes.byref(t_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return q_ptr.value, t_ptr.value


def ENsetqualtype(qual_code: int, chem_name: str, chem_units: str, trace_node: str) -> None:
    """Sets the water quality analysis parameters."""
    ierr = _lib.ENsetqualtype(qual_code,
                              ctypes.c_char_p(chem_name.encode()),
                              ctypes.c_char_p(chem_units.encode()),
                              ctypes.c_char_p(trace_node.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetoption(option_code: int) -> float:
    """Gets the value of a simulation option."""
    value_ptr = ctypes.c_float()
    ierr = _lib.ENgetoption(option_code, ctypes.byref(value_ptr))
    if ierr:
        raise ENtoolkitError(ierr)

def ENsetoption(option_code: int, value: float) -> None:
    """Sets the value of a simulation option."""
    ierr = _lib.ENsetoption(option_code, ctypes.c_float(value))
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetversion() -> int:
    """Gets the version number of the EPANET toolkit."""
    version_ptr = ctypes.c_int()
    ierr = _lib.ENgetversion(ctypes.byref(version_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return version_ptr.value


def ENsolveH() -> None:
    """Solves the hydraulics for the current project."""
    ierr = _lib.ENsolveH()
    if ierr:
        raise ENtoolkitError(ierr)


def ENopenH() -> None:
    """Opens the hydraulic solver."""
    ierr = _lib.ENopenH()
    if ierr:
        raise ENtoolkitError(ierr)


def ENinitH(init_flag: int = 0) -> None:
    """Initializes the hydraulic solver."""
    ierr = _lib.ENinitH(init_flag)
    if ierr:
        raise ENtoolkitError(ierr)


def ENrunH() -> int:
    """Executes a single step of the hydraulic simulation. Returns simulation time."""
    time_ptr = ctypes.c_long()
    ierr = _lib.ENrunH(ctypes.byref(time_ptr))
    if ierr >= 100:
        raise ENtoolkitError(ierr)
    return time_ptr.value


def ENnextH() -> int:
    """Advances one time step in the simulation. Returns time remaining."""
    deltat_ptr = ctypes.c_long()
    ierr = _lib.ENnextH(ctypes.byref(deltat_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return deltat_ptr.value


def ENcloseH() -> None:
    """Closes the hydraulic solver."""
    ierr = _lib.ENcloseH()
    if ierr:
        raise ENtoolkitError(ierr)


def ENsolveQ() -> None:
    """Solves water quality for current project."""
    ierr = _lib.ENsolveQ()
    if ierr:
        raise ENtoolkitError(ierr)


def ENopenQ() -> None:
    """Opens the quality solver."""
    ierr = _lib.ENopenQ()
    if ierr:
        raise ENtoolkitError(ierr)


def ENinitQ(init_flag: int = 0) -> None:
    """Initializes the quality solver."""
    ierr = _lib.ENinitQ(init_flag)
    if ierr:
        raise ENtoolkitError(ierr)


def ENrunQ() -> int:
    """Runs one quality simulation step. Returns time."""
    time_ptr = ctypes.c_long()
    ierr = _lib.ENrunQ(ctypes.byref(time_ptr))
    if ierr >= 100:
        raise ENtoolkitError(ierr)
    return time_ptr.value


def ENnextQ() -> int:
    """Advances one quality simulation step. Returns time remaining."""
    deltat_ptr = ctypes.c_long()
    ierr = _lib.ENnextQ(ctypes.byref(deltat_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return deltat_ptr.value


def ENcloseQ() -> None:
    """Closes quality solver."""
    ierr = _lib.ENcloseQ()
    if ierr:
        raise ENtoolkitError(ierr)


def ENsaveH() -> None:
    """Saves hydraulic results."""
    ierr = _lib.ENsaveH()
    if ierr:
        raise ENtoolkitError(ierr)


def ENsaveinpfile(file_name: str) -> None:
    """Saves current network state as an .inp file."""
    ierr = _lib.ENsaveinpfile(ctypes.c_char_p(file_name.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENsavehydfile(file_name: str) -> None:
    """Saves binary hydraulics results."""
    ierr = _lib.ENsavehydfile(ctypes.c_char_p(file_name.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENusehydfile(file_name: str) -> None:
    """Uses a pre-calculated hydraulics binary file."""
    ierr = _lib.ENusehydfile(ctypes.c_char_p(file_name.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENreport() -> None:
    """Generates the report file."""
    ierr = _lib.ENreport()
    if ierr:
        raise ENtoolkitError(ierr)


def ENresetreport() -> None:
    """Resets all report commands."""
    ierr = _lib.ENresetreport()
    if ierr:
        raise ENtoolkitError(ierr)


def ENsetreport(command: str) -> None:
    """Applies a specific report configuration command."""
    ierr = _lib.ENsetreport(ctypes.c_char_p(command.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


# --- Convenience functions for missing array exports ---

def ENgetnodevalues(property_code: int) -> List[float]:
    """Gets values for a property for all nodes via loop (legacy array export missing in 2.2)."""
    count = ENgetcount(EN_NODECOUNT)
    return [ENgetnodevalue(i, property_code) for i in range(1, count + 1)]


def ENgetlinkvalues(property_code: int) -> List[float]:
    """Gets values for a property for all links via loop (legacy array export missing in 2.2)."""
    count = ENgetcount(EN_LINKCOUNT)
    return [ENgetlinkvalue(i, property_code) for i in range(1, count + 1)]


def ENsolveH() -> None:
    """Solves the hydraulics for the current project."""
    ierr = _lib.ENsolveH()
    if ierr:
        raise ENtoolkitError(ierr)


def ENopenH() -> None:
    """Opens the hydraulic solver."""
    ierr = _lib.ENopenH()
    if ierr:
        raise ENtoolkitError(ierr)


def ENinitH(init_flag: int = 0) -> None:
    """Initializes the hydraulic solver."""
    ierr = _lib.ENinitH(init_flag)
    if ierr:
        raise ENtoolkitError(ierr)


def ENrunH() -> int:
    """Executes a single step of the hydraulic simulation. Returns simulation time."""
    time_ptr = ctypes.c_long()
    ierr = _lib.ENrunH(ctypes.byref(time_ptr))
    if ierr >= 100:
        raise ENtoolkitError(ierr)
    return time_ptr.value


def ENnextH() -> int:
    """Advances one time step in the simulation. Returns time remaining."""
    deltat_ptr = ctypes.c_long()
    ierr = _lib.ENnextH(ctypes.byref(deltat_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return deltat_ptr.value


def ENcloseH() -> None:
    """Closes the hydraulic solver."""
    ierr = _lib.ENcloseH()
    if ierr:
        raise ENtoolkitError(ierr)


def ENsolveQ() -> None:
    """Solves water quality for current project."""
    ierr = _lib.ENsolveQ()
    if ierr:
        raise ENtoolkitError(ierr)


def ENopenQ() -> None:
    """Opens the quality solver."""
    ierr = _lib.ENopenQ()
    if ierr:
        raise ENtoolkitError(ierr)


def ENinitQ(init_flag: int = 0) -> None:
    """Initializes the quality solver."""
    ierr = _lib.ENinitQ(init_flag)
    if ierr:
        raise ENtoolkitError(ierr)


def ENrunQ() -> int:
    """Runs one quality simulation step. Returns time."""
    time_ptr = ctypes.c_long()
    ierr = _lib.ENrunQ(ctypes.byref(time_ptr))
    if ierr >= 100:
        raise ENtoolkitError(ierr)
    return time_ptr.value


def ENnextQ() -> int:
    """Advances one quality simulation step. Returns time remaining."""
    deltat_ptr = ctypes.c_long()
    ierr = _lib.ENnextQ(ctypes.byref(deltat_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return deltat_ptr.value


def ENcloseQ() -> None:
    """Closes quality solver."""
    ierr = _lib.ENcloseQ()
    if ierr:
        raise ENtoolkitError(ierr)


def ENsaveH() -> None:
    """Saves hydraulic results."""
    ierr = _lib.ENsaveH()
    if ierr:
        raise ENtoolkitError(ierr)


def ENsaveinpfile(file_name: str) -> None:
    """Saves current network state as an .inp file."""
    ierr = _lib.ENsaveinpfile(ctypes.c_char_p(file_name.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENsavehydfile(file_name: str) -> None:
    """Saves binary hydraulics results."""
    ierr = _lib.ENsavehydfile(ctypes.c_char_p(file_name.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENusehydfile(file_name: str) -> None:
    """Uses a pre-calculated hydraulics binary file."""
    ierr = _lib.ENusehydfile(ctypes.c_char_p(file_name.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENreport() -> None:
    """Generates the report file."""
    ierr = _lib.ENreport()
    if ierr:
        raise ENtoolkitError(ierr)


def ENresetreport() -> None:
    """Resets all report commands."""
    ierr = _lib.ENresetreport()
    if ierr:
        raise ENtoolkitError(ierr)


def ENsetreport(command: str) -> None:
    """Applies a specific report configuration command."""
    ierr = _lib.ENsetreport(ctypes.c_char_p(command.encode()))
    if ierr:
        raise ENtoolkitError(ierr)


def ENaddcontrol(type: int, link_index: int, setting: float, node_index: int, level: float) -> int:
    """Adds a new simple control."""
    index_ptr = ctypes.c_int()
    ierr = _lib.ENaddcontrol(type, link_index, ctypes.c_float(setting),
                             node_index, ctypes.c_float(level), ctypes.byref(index_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return index_ptr.value


def ENdeletecontrol(index: int) -> None:
    """Deletes a simple control."""
    ierr = _lib.ENdeletecontrol(index)
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetcontrol(index: int) -> Tuple[int, int, float, int, float]:
    """Gets parameters for a simple control."""
    type_ptr = ctypes.c_int()
    link_ptr = ctypes.c_int()
    setting_ptr = ctypes.c_float()
    node_ptr = ctypes.c_int()
    level_ptr = ctypes.c_float()
    ierr = _lib.ENgetcontrol(index, ctypes.byref(type_ptr), ctypes.byref(link_ptr),
                             ctypes.byref(setting_ptr), ctypes.byref(node_ptr),
                             ctypes.byref(level_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return type_ptr.value, link_ptr.value, float(setting_ptr.value), node_ptr.value, float(level_ptr.value)


def ENsetcontrol(index: int, type: int, link_index: int, setting: float, node_index: int, level: float) -> None:
    """Sets parameters for a simple control."""
    ierr = _lib.ENsetcontrol(index, type, link_index, ctypes.c_float(setting),
                             node_index, ctypes.c_float(level))
    if ierr:
        raise ENtoolkitError(ierr)


def ENgetstatistic(type_code: int) -> float:
    """Gets value of a simulation statistic."""
    value_ptr = ctypes.c_float()
    ierr = _lib.ENgetstatistic(type_code, ctypes.byref(value_ptr))
    if ierr:
        raise ENtoolkitError(ierr)
    return float(value_ptr.value)


def ENgetdemandmodel() -> Tuple[int, float, float, float]:
    """Gets the demand model parameters."""
    model = ctypes.c_int()
    pmin = ctypes.c_float()
    preq = ctypes.c_float()
    pexp = ctypes.c_float()
    ierr = _lib.ENgetdemandmodel(ctypes.byref(model), ctypes.byref(pmin),
                                 ctypes.byref(preq), ctypes.byref(pexp))
    if ierr:
        raise ENtoolkitError(ierr)
    return model.value, float(pmin.value), float(preq.value), float(pexp.value)


def ENsetdemandmodel(model: int, pmin: float, preq: float, pexp: float) -> None:
    """Sets the demand model parameters."""
    ierr = _lib.ENsetdemandmodel(model, ctypes.c_float(pmin),
                                 ctypes.c_float(preq), ctypes.c_float(pexp))
    if ierr:
        raise ENtoolkitError(ierr)


def ENsetstatusreport(status_level: int) -> None:
    """Sets the level of status reporting (0, 1, or 2)."""
    ierr = _lib.ENsetstatusreport(status_level)
    if ierr:
        raise ENtoolkitError(ierr)



