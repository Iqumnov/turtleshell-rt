"""
TurtleShell Contour 3: Temporal Laser-Cooling Buffer Simulation
Численная верификация аналитической оценки τ_б ≈ 0.7 с для ионной ловушки
"""
import numpy as np
import matplotlib.pyplot as plt

# Настройка отображения русских символов и LaTeX
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Параметры из Таблицы 2 статьи
eta = 10.0       # скорость лазерного охлаждения, 1/с
n_dot = 1.0      # скорость аномального нагрева мод, фон/с
n_star = 0.2     # пороговое число фононов для безопасного сеанса

# Аналитическая формула (5) из статьи
def n_bar(tau, n_0, eta, n_dot):
    """Среднее число фононов после буфера длительности tau"""
    n_inf = n_dot / eta
    return n_inf + (n_0 - n_inf) * np.exp(-eta * tau)

# Аналитическая формула (6) для требуемого буфера
def tau_buffer(n_0, eta, n_dot, n_star):
    """Требуемая длительность буфера"""
    n_inf = n_dot / eta
    return (1.0 / eta) * np.log((n_0 - n_inf) / (n_star - n_inf))

# --- Генерация Рисунка 7 в стиле Рисунка 6 ---
tau = np.logspace(-3, 1, 1000)  # от 1 мс до 10 с
n_0_values = [10, 100, 1000]

fig, ax = plt.subplots(figsize=(10, 6))

# Стили линий в стиле Рис. 6: тонкая сплошная, жирная сплошная, штриховая
# (n_0=10 → тонкая, n_0=100 → жирная, n_0=1000 → штриховая)
line_styles = [
    (n_0_values[0], '-', 0.8, r'$\bar{n}_0 = 10$'),
    (n_0_values[1], '-', 2.0, r'$\bar{n}_0 = 100$'),
    (n_0_values[2], '--', 1.4, r'$\bar{n}_0 = 1000$'),
]

for n_0, ls, lw, label in line_styles:
    n_vals = n_bar(tau, n_0, eta, n_dot)
    ax.plot(tau, n_vals, color='black', linestyle=ls, linewidth=lw, label=label)

# Пороговая линия (тонкая штриховая, серая)
ax.axhline(y=n_star, color='black', linestyle='--', linewidth=0.8,
           label=r'$n^* = 0.2$ (порог)')

# Асимптота (штрихпунктирная, серая)
n_inf = n_dot / eta
ax.axhline(y=n_inf, color='gray', linestyle='-.', linewidth=0.7,
           label=r'$\bar{n}_\infty = \dot{n}/\eta = 0.1$')

# Отметка τ_б для типового случая (вертикальная пунктирная)
tau_typ = tau_buffer(100, eta, n_dot, n_star)
ax.axvline(x=tau_typ, color='black', linestyle=':', linewidth=1.2,
           label=r'$\tau_б \approx 0.69$ с (типовой)')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'Длительность буфера $\tau$ (с)', fontsize=12)
ax.set_ylabel(r'Среднее число фононов $\bar{n}(\tau)$', fontsize=12)
ax.set_title(
    'Численная верификация Контура 3: динамика охлаждения мод\n'
    r'(параметры: $\eta = 10$ с$^{-1}$, $\dot{n} = 1$ фон/с)',
    fontsize=13
)

# Легенда в стиле Рис. 6
ax.legend(fontsize=10, loc='upper right', frameon=True,
          facecolor='white', edgecolor='black')

ax.grid(True, which="both", ls="-", alpha=0.15)
ax.set_ylim(0.05, 2000)
ax.set_xlim(0.001, 10)

plt.tight_layout()
plt.savefig('contour3_buffer_dynamics.png', dpi=300, bbox_inches='tight')
plt.show()

# --- Численная верификация заявленных оценок ---
print("=" * 65)
print("Верификация аналитической оценки τ_б ≈ 0.7 с (формула 6)")
print("=" * 65)
for n_0 in n_0_values:
    tau_calc = tau_buffer(n_0, eta, n_dot, n_star)
    n_final = n_bar(tau_calc, n_0, eta, n_dot)
    print(f"n̄₀ = {n_0:4d} → τ_б = {tau_calc:.3f} с, "
          f"n̄(τ_б) = {n_final:.4f} (≤ n*={n_star})")
print("=" * 65)
print(f"Типовой случай (n̄₀=100): τ_б = {tau_buffer(100, eta, n_dot, n_star):.3f} с")
print("График сохранён: contour3_buffer_dynamics.png")