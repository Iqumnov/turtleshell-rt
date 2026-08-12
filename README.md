# TurtleShell-RT

**Open-source numerical verification artifact for Paper #1: "TurtleShell: A Multi-Contour Process Isolation Framework for Multi-Tenant Quantum Clouds"**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21903243.svg)](https://doi.org/10.5281/zenodo.21903243)

## Overview

This repository provides **reproducible numerical verification** of the analytical model for **Contour 3** (temporal laser-cooling buffers) from the TurtleShell multi-tenant isolation framework.

**Paper:** "TurtleShell: A Multi-Contour Process Isolation Framework for Multi-Tenant Quantum Clouds" (under review)

**Scope:** This artifact verifies the phonon-cooling dynamics model (Eqs. 5–6 in the paper) using two independent methods:
1. **Analytical solution** of the cooling ODE
2. **Independent numerical integration** via QuTiP Lindblad master equation solver (optional)

The full four-contour TurtleShell implementation is under active development and will be released as a separate repository (Paper #2).

---

## What Is Verified

### Contour 3 — Temporal Laser-Cooling Buffers

**Physical Model:** Laser cooling of trapped-ion motional modes between multi-tenant sessions to reset residual phonon excitation.

**Key Equations:**
- **Eq. (5):** Mean phonon number dynamics: `n̄(τ) = n̄_∞ + (n̄₀ − n̄_∞)·exp(−ητ)`, where `n̄_∞ = /η`
- **Eq. (6):** Required buffer duration: `τ_b = (1/η)·ln[(n̄₀ − /η)/(n* − ṅ/η)]`

**Parameters** (Table 2 in paper):
- `η = 10 s⁻¹` (laser cooling rate)
- `ṅ = 1 phonon/s` (anomalous heating rate)
- `n* = 0.2` (threshold for safe session)

**Result:** At typical parameters (n̄₀ = 100), the analytical estimate gives **τ_b ≈ 0.691 s**, verified numerically to machine precision (~10⁻⁶ relative error).

---

## Quick Start

### Requirements

**Core dependencies:**
- Python 3.8+
- NumPy ≥ 1.24
- Matplotlib ≥ 3.7

**Optional (for independent QuTiP verification):**
- QuTiP ≥ 5.0 (recommended for full reproducibility)

### Installation

```bash
git clone https://github.com/iqumnov/turtleshell-rt.git
cd turtleshell-rt

pip install numpy matplotlib

# Optional: independent QuTiP verification
pip install qutip
```

### Running the Verification

```bash
python turtleshell_contour3.py
```

**Output:**
- `contour3_buffer_duration.png` — Fig. 6 in paper
- `contour3_buffer_dynamics.png` — Fig. 7 in paper
- `figure7_data.csv` — reproducibility data
- `figure7_qutip.csv` — QuTiP reference (if QuTiP is installed)
- Console verification report

### Expected Console Output

```text
=================================================================
Verification of the analytical estimate τ_b ≈ 0.7 s (Eq. 6)
=================================================================
n̄₀ =   10 → τ_b = 0.460 s, n̄(τ_b) = 0.2000 (≤ n*=0.2)
n̄₀ =  100 → τ_b = 0.691 s, n̄(τ_b) = 0.2000 (≤ n*=0.2)
n̄₀ = 1000 → τ_b = 0.921 s, n̄(τ_b) = 0.2000 (≤ n*=0.2)
=================================================================
Typical case (n̄₀=100): τ_b = 0.691 s
Max. deviation of QuTiP from analytics: ~1e-06
=================================================================
```

---

## Reproducibility

### Deterministic Execution

This code is **fully deterministic**:
- No random number generation
- No platform-dependent operations
- Results are bit-reproducible across runs and systems

### Control Numbers

For independent verification, the following values should be reproduced exactly:

| Parameter | Value | Source |
|---|---|---|
| τ_b (n̄₀ = 100) | 0.6908 s | Eq. (6) |
| n̄_∞ | 0.1 phonons | ṅ/η |
| Relative error (analytical vs QuTiP) | < 10⁻⁶ | Machine precision |

### QuTiP Verification (Optional)

If QuTiP is installed, the script independently integrates the Lindblad master equation:

```text
dρ/dt = Σ_k [ L_k ρ L_k† − ½ {L_k† L_k, ρ} ]
```

with collapse operators:
- `L_1 = √η · a` (laser cooling)
- `L_2 = √ṅ · a†` (anomalous heating)

The QuTiP solution should match the analytical formula (Eq. 5) to within **~10⁻⁶ relative error**, confirming the physical model's correctness.

---

## Repository Structure

```text
turtleshell-rt/
├── README.md                        # this file
├── LICENSE                          # MIT License
├── turtleshell_contour3.py          # main verification script
├── tests/
│   └── test_contour3.py             # unit tests
├── requirements.txt                 # Python dependencies
├── contour3_buffer_duration.png     # Fig. 6 (generated)
├── contour3_buffer_dynamics.png     # Fig. 7 (generated)
├── figure7_data.csv                 # reproducibility data
└── figure7_qutip.csv                # QuTiP reference (optional)
```

---

## Testing

```bash
pytest -q
```

The test suite verifies:
1. Analytical formula consistency (Eq. 6 derived from Eq. 5)
2. Threshold reached exactly: `n̄(τ_b) = n*` for all test cases
3. Monotonicity: larger n̄₀ → larger τ_b
4. Unreachable threshold raises `ValueError` (n* ≤ ṅ/η)
5. QuTiP agreement (if available, max deviation < 10⁻⁶)

---

## Limitations and Scope

### What This Artifact Does NOT Include

This repository is **specifically for Paper #1 verification** and does NOT include:
- Full four-contour TurtleShell implementation (Contours 1, 2, 4)
- Multi-platform QPU simulator (IBM Eagle, Heron, etc.)
- Attack scenario implementations (crosstalk, rowhammer, etc.)
- Economic model (TCO, ROI calculations)

These components are under development and will be released as **Paper #2** (SoftwareX/JOSS submission).

### Physical Model Assumptions

The verification assumes:
- Linear cooling dynamics (valid for laser sideband cooling in the Lamb–Dicke regime)
- Constant heating rate ṅ (valid for surface-electrode traps near room temperature)
- Single-mode approximation (valid for well-separated motional modes)

For deviations from these assumptions, see Section 5.3 (Limitations) in the paper.

---

## Citation

If you use this code or the underlying methodology, please cite:

```bibtex
@article{igumnov2026turtleshell,
  title     = {TurtleShell: A Multi-Contour Process Isolation Framework
               for Multi-Tenant Quantum Clouds},
  author    = {Igumnov, Matvei and Kostin, Dmitry and Pitelinsky, Kirill},
  journal   = {[Journal Name]},
  year      = {2026},
  note      = {Under review}
}
```

*Update the `journal` and `year` fields once the paper is published.*

---

## Contributing

Contributions are welcome. Please:

1. **Open an issue** first to discuss proposed changes
2. **Follow PEP 8** with type hints on public functions
3. **Add tests** for any new functionality
4. **Update documentation** (this README and inline docstrings)

### Development Setup

```bash
git clone https://github.com/iqumnov/turtleshell-rt.git
cd turtleshell-rt

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
pip install qutip pytest        # optional, recommended

python turtleshell_contour3.py
pytest -q
```

---

## Contact

- **Matvei Igumnov** (lead developer) — `iqumnov@proton.me`
- **Dmitry Kostin** (co-developer) — `rjurt122@yandex.ru`
- **Kirill Pitelinsky** (supervisor) — `yekadath@gmail.com`

**Affiliation:** Moscow Polytechnic University, Department of Information Security

---

## Acknowledgments

This work was supported by the **Moscow Polytechnic University** as part of the core research program.

The authors thank the anonymous reviewers for constructive feedback that improved the clarity of the physical model.

---

**Last updated:** August 2026  
**Version:** 1.0.0 (Paper #1 artifact release)  
**License:** MIT (see `LICENSE`)
