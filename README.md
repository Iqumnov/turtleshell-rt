# TurtleShell-RT

Open-source numerical verification of the **TurtleShell** multi-tenant isolation 
framework for trapped-ion and neutral-atom quantum information systems.

This repository contains the numerical verification of **Contour 3** (temporal 
laser-cooling buffers). 
The full four-contour implementation is under active development.

## What Is Implemented

- **Contour 3 — Temporal laser-cooling buffers**: numerical integration of the 
  phonon-cooling dynamics between multi-tenant sessions, verifying the 
  analytical estimate τ_b ≈ 0.7 s at typical trapped-ion parameters.

### Planned (upcoming releases)

- Contour 1 — Physical partitioning + adaptive RF filtering
- Contour 2 — Pulse-sequence verification (SHA-256 of compilation graph)
- Contour 4 — Differential telemetry monitoring (synthetic-frequency method)
- Full System — A fully compiled ready-to-use system with all the developed tools and methods included

## Quick Start

### Requirements

- Python 3.8+
- NumPy
- Matplotlib

### Installation

```bash
pip install numpy matplotlib
git clone https://github.com/iqumnov/turtleshell-rt.git
```

### Running

```bash
cd turtleshell-rt
python turtleshell_contour3.git
```

The script produces:
A publication-quality figure saved as contour3_buffer_dynamics.png
Console output with numerical verification of τ_b for n̄₀ = 10, 100, 1000

# Expected Output

```
=================================================================
Verification of the analytical estimate τ_b ≈ 0.7 s (Eq. 6)
=================================================================
n̄₀ =   10 → τ_b = 0.460 s, n̄(τ_b) = 0.2000 (≤ n*=0.2)
n̄₀ =  100 → τ_b = 0.691 s, n̄(τ_b) = 0.2000 (≤ n*=0.2)
n̄₀ = 1000 → τ_b = 0.921 s, n̄(τ_b) = 0.2000 (≤ n*=0.2)
=================================================================
Typical case (n̄₀=100): τ_b = 0.691 s
```
# Repository Structure

turtle-shell-rt/
├── README.md                       # this file
├── turtleshell_contour3.py         # Contour 3 numerical verification
└── contour3_buffer_dynamics.png    # output figure

# Contributing

Contributions are welcome. Please open an issue first to discuss proposed changes.

# Contact

Matvei Igumnov — iqumnov@proton.me
Dmitry Kostin — rjurt122@yandex.ru
Kirill Pitelinsky — yekadath@gmail.com

# MIT License
