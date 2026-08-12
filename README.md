# TurtleShell-RT

**Open-source numerical verification artifact for Paper #1: "TurtleShell: A Multi-Contour Process Isolation Framework for Multi-Tenant Quantum Clouds"**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

## Overview

This repository provides **reproducible numerical verification** of the analytical model for **Contour 3** (temporal laser-cooling buffers) from the TurtleShell multi-tenant isolation framework.

**Paper:** "TurtleShell: A Multi-Contour Process Isolation Framework for Multi-Tenant Quantum Clouds" (under review)

**Scope:** This artifact verifies the phonon-cooling dynamics model (Eqs. 5-6 in the paper) using two independent methods:
1. **Analytical solution** of the cooling ODE
2. **Independent numerical integration** via QuTiP Lindblad master equation solver (optional)

The full four-contour TurtleShell implementation is under active development and will be released as a separate repository (Paper #2).

---

## What Is Verified

### Contour 3 — Temporal Laser-Cooling Buffers

**Physical Model:** Laser cooling of trapped-ion motional modes between multi-tenant sessions to reset residual phonon excitation.

**Key Equations:**
- **Eq. (5):** Mean phonon number dynamics: `n̄(τ) = n̄_∞ + (n̄₀ - n̄_∞)·exp(-ητ)`, where `n̄_∞ = ṅ/η`
- **Eq. (6):** Required buffer duration: `τ_b = (1/η)·ln[(n̄₀ - ṅ/η)/(n* - ṅ/η)]`

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
# Clone repository
git clone https://github.com/iqumnov/turtleshell-rt.git
cd turtleshell-rt

# Install core dependencies
pip install numpy matplotlib

# Optional: Install QuTiP for independent verification
pip install qutip
