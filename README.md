# entoolkit

Python extension for the **EPANET 2.2** Programmer Toolkit.

`entoolkit` provides a Pythonic wrapper around the EPANET hydraulic simulation engine. It includes two distinct APIs to suit different needs:
1. **Legacy API (`toolkit.py`)**: A direct 1-to-1 mapping of the traditional EPANET functions (global state).
2. **Handle-Based API (`EPANETProject`)**: A modern, thread-safe, and high-precision interface (64-bit) that allows managing multiple projects simultaneously.

---

## Installation

Currently, you can install the package by cloning the repository and running:

```bash
pip install .
```

The package comes pre-bundled with 64-bit and 32-bit binaries for **Windows**, **Linux**, and **macOS** (Intel & Apple Silicon).

---

## Quick Start

### 1. Thread-Safe API (Recommended)
This API uses the new EPANET 2.2 handle system and supports `double` precision.

```python
from entoolkit import EPANETProject, EN_PRESSURE

# Create a new project instance
proj = EPANETProject()

# Open a network file
proj.open("networks/Net1.inp", "report.rpt", "out.bin")

# Solve hydraulics
proj.solveH()

# Retrieve pressures for all nodes (efficiently)
pressures = proj.getnodevalues(EN_PRESSURE)

# Close and free memory
proj.close()
proj.delete()
```

### 2. Legacy API
Identical to the classic EPANET C API.

```python
from entoolkit import toolkit

toolkit.ENopen("networks/Net1.inp")
toolkit.ENsolveH()
p = toolkit.ENgetnodevalue(1, toolkit.EN_PRESSURE)
toolkit.ENclose()
```

---

## What's New in 2.2
- **Multiple Demands**: Support for multiple demand categories per junction.
- **Advanced Controls**: New rule-based control functions.
- **Pressure Dependent Demands (PDA)**: Direct support for PDA simulation models.
- **High Precision**: The handle-based API uses 64-bit doubles for all physical properties.

---

## Running Tests
The package includes a comprehensive test suite in `run_tests.py`.

```bash
python run_tests.py
```

---

## Origin and Credits

The binaries included in this package are derived from:
1. **Open Water Analytics (OWA) EPANET**: The official community-driven EPANET 2.2 engine. [GitHub Repo](https://github.com/OpenWaterAnalytics/EPANET)
2. **WNTR (US EPA)**: Some platform-specific binaries and network examples were adapted from the Water Network Tool for Resilience. [WNTR GitHub](https://github.com/USEPA/WNTR)

### Citation
If you use this toolkit in your research, please cite the original EPANET engine:
> Rossman, L. A. (2000). EPANET 2: users manual. U.S. Environmental Protection Agency, Cincinnati, OH, EPA/600/R-00/057.

And the OWA community for the 2.2 upgrade:
> Open Water Analytics. (2020). EPANET 2.2.0. https://github.com/OpenWaterAnalytics/EPANET

---

## License

The `entoolkit` wrapper is licensed under the **GNU General Public License v2 (GPLv2)**. 
Bundled EPANET binaries are subject to their respective licenses (Public Domain / MIT / BSD), which are compatible with GPLv2 for redistribution.

---

## Documentation
- [Official EPANET 2.2 Manual](https://epanet22.readthedocs.io/)
- [EPANET 2.2 Toolkit API Reference](https://github.com/OpenWaterAnalytics/EPANET/wiki/EPANET-2.2-Toolkit-Functions)
