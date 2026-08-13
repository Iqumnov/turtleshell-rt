
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

# English

**Open-source numerical verification artifact for: "Turtle Shell (TurtleShell):
A Multi-Level Isolation System for Multi-User Quantum Information Systems Based on
Trapped Particles".**

## Overview

TurtleShell Demo provides **reproducible numerical verification** of the analytical
model for **Contour 3** (temporal laser-cooling buffers) from the TurtleShell
multi-tenant isolation framework.

**Scope:** This artifact verifies the phonon-cooling dynamics model (Eqs. 5–6 in the
paper) using two independent methods:
1. **Analytical solution** of the cooling ODE;
2. **Independent numerical integration** via the QuTiP Lindblad master-equation solver (optional).

The full four-contour TurtleShell implementation is under active development and will
be released as a separate repository.

## What Is Verified

### Contour 3 — Temporal Laser-Cooling Buffers

**Physical Model:** Laser cooling of trapped-ion motional modes between multi-tenant
sessions to reset residual phonon excitation.

**Key Equations:**
- **Eq. (5):** Mean phonon number dynamics: `n̄(τ) = n̄_∞ + (n̄₀ − n̄_∞)·exp(−ητ)`, where `n̄_∞ = ṅ/η`
- **Eq. (6):** Required buffer duration: `τ_b = (1/η)·ln[(n̄₀ − ṅ/η)/(n* − ṅ/η)]`

**Parameters** (Table 2 in paper):
- `η = 10 s⁻¹` (laser cooling rate)
- `ṅ = 1 phonon/s` (anomalous heating rate)
- `n* = 0.2` (threshold for safe session)

**Result:** At typical parameters (n̄₀ = 100), the analytical estimate gives
**τ_b = 0.6906754779 s** (exactly `0.1·ln 999`), and the independent QuTiP Lindblad
solution reproduces the analytical curve with a maximum deviation below **10⁻⁶**.

## Quick Start

### Requirements

**Core dependencies:** Python 3.8+, NumPy ≥ 1.24, Matplotlib ≥ 3.7.
**Optional (independent QuTiP verification):** QuTiP ≥ 4.7 (tested with 4.x and 5.x).

### Installation

```bash
git clone https://github.com/iqumnov/turtleshell-demo.git
cd turtleshell-demo
pip install numpy matplotlib
pip install qutip   # optional
```

### Running the Verification

```bash
python turtleshell_contour3.py
```

**Output:**
- `contour3_buffer_dynamics.png` — Fig. 7 in paper (analytical curves + QuTiP points);
- `figure6_data_n10.csv`, `figure6_data_n100.csv`, `figure6_data_n1000.csv` — data to draw Fig. 6 in LaTeX/pgfplots;
- `figure7_data.csv` — reproducibility data (analytical curves);
- `figure7_qutip.csv` — QuTiP reference curve (if QuTiP is installed);
- Console verification report with built-in assertions.

**Note:** Fig. 6 is rendered in the paper via LaTeX/pgfplots from the generated CSV
data; the script does not emit a Fig. 6 PNG.

## Reproducibility

### Deterministic Execution

This code is **fully deterministic**: no random number generation, no
platform-dependent operations, bit-reproducible across runs and systems.

### Control Numbers

| Parameter | Value | Source |
|---|---|---|
| τ_b (n̄₀ = 100) | 0.6906754779 s | Eq. (6), exact `0.1·ln 999` |
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

starting from the Fock state |n̄₀ = 100⟩. The QuTiP solution matches Eq. (5) to within **10⁻⁶**.

## Repository Structure

```text
turtleshell-demo/
├── README.md                        # this file
├── LICENSE                          # MIT License
├── CITATION.cff                     # citation metadata
├── turtleshell_contour3.py          # main verification script
├── tests/
│   └── test_contour3.py             # unit tests
├── requirements.txt                 # Python dependencies
├── contour3_buffer_dynamics.png     # Fig. 7 (generated)
├── figure6_data_n10.csv             # Fig. 6 data (generated)
├── figure6_data_n100.csv            # (generated)
├── figure6_data_n1000.csv           # (generated)
├── figure7_data.csv                 # reproducibility data (generated)
└── figure7_qutip.csv                # QuTiP reference (generated, optional)
```

## Testing

```bash
pytest -q
```

The test suite verifies:
1. Analytical formula consistency (Eq. 6 reproduces the threshold n* exactly);
2. Exact buffer time: `τ_b(100) = 0.1·ln 999` to 10⁻⁹;
3. Monotonicity: larger n̄₀ → larger τ_b;
4. Unreachable threshold raises `ValueError` (n* ≤ ṅ/η).

## Limitations and Scope

This repository ships **only** the Contour-3 verification. It does NOT
include the full four-contour runtime, multi-platform QPU simulator, attack scenarios,
or the economic model.

Physical assumptions: linear cooling (Lamb–Dicke regime), constant heating rate ṅ,
single-mode approximation. See Section 5.3 of the paper.

## Contributing

Open an issue first; follow PEP 8; add tests; update documentation.

## Contact

- **Matvei Igumnov** (developer) — `iqumnov@proton.me`
- **Kirill Pitelinsky** (supervisor) — `yekadath@gmail.com`

**Affiliation:** Moscow Polytechnic University, Department of Information Security

## Acknowledgments

This work was supported by the Moscow Polytechnic University as part of the core
research program. The authors thank the anonymous reviewers for constructive feedback
that improved the clarity of the physical model.

**Last updated:** August 2026 · **Version:** 1.0.0 · **License:** MIT (see `LICENSE`)

---

# Русский

**Открытый артефакт численной верификации для: «Черепаший панцирь
(TurtleShell): многоуровневая система изоляции многопользовательских квантовых
информационных систем на основе удерживаемых частиц».**

## Обзор

TurtleShell Demo предоставляет **воспроизводимую численную верификацию** аналитической
модели **Контура 3** (временны́е буферы лазерного охлаждения) многопользовательской
системы изоляции TurtleShell.

**Область применения:** артефакт верифицирует модель динамики охлаждения фононов
(уравнения (5)–(6) статьи) двумя независимыми методами:
1. **Аналитическое решение** ОДУ охлаждения;
2. **Независимое численное интегрирование** уравнения Линдблада в QuTiP (опционально).

Полная реализация всех четырёх контуров TurtleShell находится в активной разработке и
будет выпущена отдельным репозиторием.

## Что верифицируется

### Контур 3 — Временны́е буферы лазерного охлаждения

**Физическая модель:** лазерное охлаждение колебательных мод захваченных ионов между
сеансами разных пользователей для сброса остаточного фононного возбуждения.

**Ключевые уравнения:**
- **Ур. (5):** динамика среднего числа фононов: `n̄(τ) = n̄_∞ + (n̄₀ − n̄_∞)·exp(−ητ)`, где `n̄_∞ = /η`
- **Ур. (6):** требуемая длительность буфера: `τ_b = (1/η)·ln[(n̄₀ − ṅ/η)/(n* − ṅ/η)]`

**Параметры** (Таблица 2 статьи):
- `η = 10 с⁻¹` (скорость лазерного охлаждения)
- `ṅ = 1 фон/с` (скорость аномального нагрева)
- `n* = 0.2` (порог безопасного сеанса)

**Результат:** при типовых параметрах (n̄₀ = 100) аналитическая оценка даёт
**τ_b = 0.6906754779 с** (точно `0.1·ln 999`), а независимое решение Линдблада в QuTiP
воспроизводит аналитическую кривую с максимальным отклонением менее **10⁻⁶**.

## Быстрый старт

### Требования

**Базовые зависимости:** Python 3.8+, NumPy ≥ 1.24, Matplotlib ≥ 3.7.
**Опционально:** QuTiP ≥ 4.7 (протестировано с 4.x и 5.x).

### Установка

```bash
git clone https://github.com/iqumnov/turtleshell-demo.git
cd turtleshell-demo
pip install numpy matplotlib
pip install qutip   # опционально
```

### Запуск верификации

```bash
python turtleshell_contour3.py
```

**Выходные файлы:**
- `contour3_buffer_dynamics.png` — Рис. 7 статьи (аналитические кривые + точки QuTiP);
- `figure6_data_n10.csv`, `figure6_data_n100.csv`, `figure6_data_n1000.csv` — данные для Рис. 6 (LaTeX/pgfplots);
- `figure7_data.csv` — данные воспроизводимости (аналитика);
- `figure7_qutip.csv` — опорная кривая QuTiP (если установлен);
- консольный отчёт верификации со встроенными утверждениями.

**Примечание:** Рис. 6 в статье отрисовывается через LaTeX/pgfplots из сгенерированных
CSV; скрипт не создаёт PNG для Рис. 6.

## Воспроизводимость

Код **полностью детерминирован**: без генератора случайных чисел, без
платформозависимых операций, побитово воспроизводим между запусками и системами.

### Контрольные числа

| Параметр | Значение | Источник |
|---|---|---|
| τ_b (n̄₀ = 100) | 0.6906754779 с | Ур. (6), точно `0.1·ln 999` |
| τ_b (n̄₀ = 10) | 0.4595119850 с | Ур. (6) |
| τ_b (n̄₀ = 1000) | 0.9210240367 с | Ур. (6) |
| n̄_∞ | 0.1 фононов | ṅ/η |
| макс. \|n̄_QuTiP − n̄_аналитика\| | < 10⁻⁶ | независимый расчёт Линдблада |

### QuTiP-верификация (опционально)

При установленном QuTiP скрипт независимо интегрирует уравнение Линдблада с операторами
коллапса из уравнения (2) статьи: `L_1 = √η·a` (охлаждение), `L_2 = √ṅ·a` и
`L_3 = √ṅ·a†` (симметричная пара нагрева, дающая dn̄/dt = +ṅ), начиная с фоковского
состояния |n̄₀ = 100⟩. Решение совпадает с ур. (5) с точностью до **10⁻⁶**.

## Структура репозитория

```text
turtleshell-demo/
├── README.md                        # этот файл
├── LICENSE                          # лицензия MIT
├── CITATION.cff                     # метаданные цитирования
├── turtleshell_contour3.py          # основной скрипт верификации
├── tests/
│   └── test_contour3.py             # юнит-тесты
├── requirements.txt                 # зависимости Python
├── contour3_buffer_dynamics.png     # Рис. 7 (генерируется)
├── figure6_data_n10.csv             # данные Рис. 6 (генерируется)
├── figure6_data_n100.csv            # (генерируется)
├── figure6_data_n1000.csv           # (генерируется)
├── figure7_data.csv                 # данные воспроизводимости (генерируется)
└── figure7_qutip.csv                # опорная кривая QuTiP (генерируется, опц.)
```

## Тестирование

```bash
pytest -q
```

Тесты проверяют: согласованность формул (ур. 6 точно воспроизводит порог n*); точное
время буфера `τ_b(100) = 0.1·ln 999` с точностью 10⁻⁹; монотонность (больше n̄₀ →
больше τ_b); недостижимый порог вызывает `ValueError` (n* ≤ ṅ/η).

## Ограничения и область применения

Репозиторий содержит **только** верификацию Контура 3. Полная
четырёхконтурная система, мультиплатформенный симулятор QPU, сценарии атак и
экономическая модель сюда не входят.

Физические допущения: линейное охлаждение (режим Лэмба–Дике), постоянная скорость
нагрева ṅ, одномодовое приближение. См. раздел 5.3 статьи.

## Участие

Сначала откройте issue; следуйте PEP 8; добавляйте тесты; обновляйте документацию.

## Контакты

- **Матвей Игумнов** (разработчик) — `iqumnov@proton.me`
- **Кирилл Пителинский** (научный руководитель) — `yekadath@gmail.com`

**Аффилиация:** Московский политехнический университет, кафедра «Информационная безопасность».

## Благодарности

Работа выполнена в рамках базовой части научной деятельности Московского
политехнического университета. Авторы благодарят анонимных рецензентов за конструктивные
замечания, позволившие улучшить ясность изложения физической модели.

**Обновлено:** август 2026 · **Версия:** 1.0.0 · **Лицензия:** MIT (см. `LICENSE`)
