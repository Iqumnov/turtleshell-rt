# TurtleShell-RT

**Open-source numerical verification artifact for Paper #1: "TurtleShell: A Multi-Contour Process Isolation Framework for Multi-Tenant Quantum Clouds"**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

This repository provides **reproducible numerical verification** of the analytical model for **Contour 3** (temporal laser-cooling buffers) from the TurtleShell multi-tenant isolation framework.

**Paper:** "TurtleShell: A Multi-Contour Process Isolation Framework for Multi-Tenant Quantum Clouds" (under review)

**Scope:** This artifact verifies the phonon-cooling dynamics model (Eqs. 5–6 in the paper) using two independent methods:
1. **Analytical solution** of the cooling ODE
2. **Independent numerical integration** via the QuTiP Lindblad master-equation solver (optional)

The full four-contour TurtleShell implementation is under active development and will be released as a separate repository (Paper #2).

---

## What Is Verified

### Contour 3 — Temporal Laser-Cooling Buffers

**Physical Model:** Laser cooling of trapped-ion motional modes between multi-tenant sessions to reset residual phonon excitation.

**Key Equations:**
- **Eq. (5):** Mean phonon number dynamics: `n̄(τ) = n̄_∞ + (n̄₀ − n̄_∞)·exp(−ητ)`, where `n̄_∞ = ṅ/η`
- **Eq. (6):** Required buffer duration: `τ_b = (1/η)·ln[(n̄₀ − ṅ/η)/(n* − ṅ/η)]`

**Parameters** (Table 2 in paper):
- `η = 10 s⁻¹` (laser cooling rate)
- `ṅ = 1 phonon/s` (anomalous heating rate)
- `n* = 0.2` (threshold for safe session)

**Result:** At typical parameters (n̄₀ = 100), the analytical estimate gives **τ_b = 0.6906754779 s** (exactly `0.1·ln 999`), and the independent QuTiP Lindblad solution reproduces the analytical curve with a maximum deviation below **10⁻⁶**.

---

## Quick Start

### Requirements

**Core dependencies:**
- Python 3.8+
- NumPy ≥ 1.24
- Matplotlib ≥ 3.7

**Optional (for independent QuTiP verification):**
- QuTiP ≥ 4.7 (tested with 4.x and 5.x; recommended for full reproducibility)

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
- `contour3_buffer_dynamics.png` — Fig. 7 in paper (analytical curves + QuTiP points)
- `figure6_data_n10.csv`, `figure6_data_n100.csv`, `figure6_data_n1000.csv` — data to draw Fig. 6 in LaTeX/pgfplots
- `figure7_data.csv` — reproducibility data (analytical curves)
- `figure7_qutip.csv` — QuTiP reference curve (if QuTiP is installed)
- Console verification report with built-in assertions

**Note:** Fig. 6 is rendered in the paper via LaTeX/pgfplots from the generated CSV data; the script does not emit a Fig. 6 PNG.

### Expected Console Output

```text
Генерация материалов для статьи TurtleShell...

✓ figure6_data_n10.csv сохранён (для LaTeX/pgfplots)
✓ figure6_data_n100.csv сохранён (для LaTeX/pgfplots)
✓ figure6_data_n1000.csv сохранён (для LaTeX/pgfplots)
Рисунок 7: запускаем QuTiP (высокая точность)...
  QuTiP: N=250 (n_0=100)
  QuTiP: решено за ~15 с
✓ Рисунок 7 сохранён: contour3_buffer_dynamics.png
======================================================================
Верификация аналитической оценки τ_б ≈ 0.7 с (формула 6)
======================================================================
n̄₀ =   10 → τ_б = 0.4595119850 с, n̄(τ_б) = 0.2000
n̄₀ =  100 → τ_б = 0.6906754779 с, n̄(τ_б) = 0.2000
n̄₀ = 1000 → τ_б = 0.9210240367 с, n̄(τ_б) = 0.2000
Макс. отклонение QuTiP от аналитики: ~1e-07
======================================================================

✓ Готово.
```

(If QuTiP is not installed, the script runs in analytics-only mode and states so explicitly.)

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
| τ_b (n̄₀ = 100) | 0.6906754779 s | Eq. (6), exact value `0.1·ln 999` |
| τ_b (n̄₀ = 10) | 0.4595119850 s | Eq. (6) |
| τ_b (n̄₀ = 1000) | 0.9210240367 s | Eq. (6) |
| n̄_∞ | 0.1 phonons | ṅ/η |
| max \|n̄_QuTiP − n̄_analytical\| | < 10⁻⁶ | independent Lindblad solve |

### QuTiP Verification (Optional)

If QuTiP is installed, the script independently integrates the Lindblad master equation

```text
dρ/dt = Σ_k [ L_k ρ L_k† − ½ {L_k† L_k, ρ} ]
```

with the collapse operators of Eq. (2) in the paper:

- `L_1 = √η · a` (laser cooling)
- `L_2 = √ṅ · a` and `L_3 = √ṅ · a†` (symmetric heating pair, giving dn̄/dt = +ṅ)

starting from the Fock state |n̄₀ = 100⟩. The QuTiP solution matches the analytical formula (Eq. 5) to within **10⁻⁶**, confirming the physical model.

---

## Repository Structure

```text
turtleshell-rt/
├── README.md                        # this file
├── LICENSE                          # MIT License
├── CITATION.cff                     # citation metadata
├── turtleshell_contour3.py          # main verification script
├── tests/
│   └── test_contour3.py             # unit tests
├── requirements.txt                 # Python dependencies
├── contour3_buffer_dynamics.png     # Fig. 7 (generated)
├── figure6_data_n10.csv             # Fig. 6 data for LaTeX/pgfplots (generated)
├── figure6_data_n100.csv            # (generated)
├── figure6_data_n1000.csv           # (generated)
├── figure7_data.csv                 # reproducibility data (generated)
└── figure7_qutip.csv                # QuTiP reference (generated, optional)
```

---

## Testing

```bash
pytest -q
```

The test suite verifies:
1. Analytical formula consistency (Eq. 6 reproduces the threshold n* exactly)
2. Exact buffer time: `τ_b(100) = 0.1·ln 999` to 10⁻⁹
3. Monotonicity: larger n̄₀ → larger τ_b
4. Unreachable threshold raises `ValueError` (n* ≤ ṅ/η)

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

- **Matvei Igumnov** (developer) — `iqumnov@proton.me`
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
