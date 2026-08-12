"""
TurtleShell — Contour 3 Numerical Verification (Paper #1 artifact, Figs. 6–7)
=============================================================================

Двухметодная верификация модели буфера лазерного охлаждения:

  Метод A (аналитика):  формулы (5)–(6) статьи.
  Метод B (численный):  уравнение Линдблада для бозонной моды (QuTiP)
                        с диссипаторами sqrt(eta)*a (охлаждение) и
                        sqrt(n_dot)*a^dag (нагрев) — НЕЗАВИСИМО от аналитики.

Если QuTiP не установлен, метод B аккуратно пропускается; режим явно
помечается в консоли (в подписи Рис. 7 это учтено).

Параметры (Таблица 2): eta = 10 1/с, n_dot = 1 фон/с, n* = 0.2.

Запуск:  python contour3_verification.py
Выход:   contour3_buffer_duration.png  (Рис. 6)
         contour3_buffer_dynamics.png  (Рис. 7)
         figure7_data.csv              (данные для воспроизводимости)
         figure7_qutip.csv             (если установлен QuTiP)

Детерминизм: случайных чисел нет; результат побитово воспроизводим.
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

# ── Физические параметры (Таблица 2 статьи) ──────────────────────────────────
ETA    = 10.0   # скорость лазерного охлаждения, 1/с
N_DOT  = 1.0    # скорость аномального нагрева мод, фон/с
N_STAR = 0.2    # пороговое число фононов безопасного сеанса


# ── Метод A: аналитика ────────────────────────────────────────────────────────
def n_bar(tau, n_0, eta=ETA, n_dot=N_DOT):
    """Формула (5): среднее число фононов после буфера длительности tau."""
    n_inf = n_dot / eta
    return n_inf + (n_0 - n_inf) * np.exp(-eta * tau)


def tau_buffer(n_0, eta=ETA, n_dot=N_DOT, n_star=N_STAR):
    """Формула (6): длительность буфера до достижения порога n*.

    Raises: ValueError, если n* <= n_dot/eta (порог физически недостижим).
    """
    n_inf = n_dot / eta
    if n_star <= n_inf:
        raise ValueError(f"n*={n_star} must exceed n_inf={n_inf:.3f}")
    return (1.0 / eta) * np.log((n_0 - n_inf) / (n_star - n_inf))


# ── Метод B: независимое Линдблад-моделирование (QuTiP) ──────────────────────
def qutip_cooling_curve(n_0, tau_max=1.0, N=300):
    """Численное решение уравнения Линдблада для бозонной моды:

    dρ/dt = Σ_k [ L_k ρ L_k† − ½{L_k† L_k, ρ} ],
    L_1 = sqrt(eta)·a (охлаждение), L_2 = sqrt(n_dot)·a† (нагрев).

    Возвращает (times, n(t)); (None, None), если QuTiP отсутствует.
    """
    try:
        import qutip as qt
    except ImportError:
        return None, None
    N = max(N, int(10 * n_0))          # защита от усечения теплового состояния
    a = qt.destroy(N)
    H = 0 * a.dag() * a                # свободная мода (вращающаяся рамка)
    c_ops = [np.sqrt(ETA) * a, np.sqrt(N_DOT) * a.dag()]
    times = np.linspace(0.0, tau_max, 200)
    rho0 = qt.thermal_dm(N, n_0) if n_0 > 0 else qt.basis(N, 0).proj()
    res = qt.mesolve(H, rho0, times, c_ops, [a.dag() * a])
    return times, np.asarray(res.expect[0], dtype=float)


# ── Рисунок 6 ─────────────────────────────────────────────────────────────────
def generate_figure6():
    """Рис. 6: τ_б(ṅ) с физической асимптотой ṅ = n*η."""
    n_dot_range = np.logspace(-2, 1, 200)
    fig, ax = plt.subplots(figsize=(10, 6))

    for n_0, ls, lw in [(10, "-", 0.8), (100, "-", 2.0), (1000, "--", 1.4)]:
        tau_vals = np.array([
            tau_buffer(n_0, n_dot=nd) if nd < N_STAR * ETA else np.nan
            for nd in n_dot_range
        ])
        ax.plot(n_dot_range, tau_vals, color="black", ls=ls, lw=lw,
                label=rf"$\bar{{n}}_0 = {n_0}$")

    ax.axvline(x=N_STAR * ETA, color="gray", ls="--", lw=0.8,
               label=r"$\dot{n} = n^*\eta = 2$ с$^{-1}$ (буфер невозможен)")
    ax.axhline(y=tau_buffer(100), color="black", ls=":", lw=1.2,
               label=r"$\tau_б \approx 0.69$ с (типовые параметры)")

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"Скорость нагрева $\dot{n}$ (фон/с)", fontsize=12)
    ax.set_ylabel(r"Длительность буфера $\tau_б$ (с)", fontsize=12)
    ax.set_title("Рисунок 6: длительность буфера как функция скорости нагрева\n"
                 r"(параметры: $\eta = 10$ с$^{-1}$, $n^* = 0.2$)", fontsize=13)
    ax.legend(fontsize=10, loc="upper left")
    ax.grid(True, which="both", ls="-", alpha=0.15)
    ax.set_xlim(0.01, 10); ax.set_ylim(0.01, 10)

    plt.tight_layout()
    plt.savefig("contour3_buffer_duration.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✓ Рисунок 6 сохранён: contour3_buffer_duration.png")


# ── Рисунок 7 ─────────────────────────────────────────────────────────────────
def generate_figure7():
    """Рис. 7: динамика n̄(τ) + независимая QuTiP-кривая + CSV-дамп."""
    tau = np.logspace(-3, 1, 1000)
    fig, ax = plt.subplots(figsize=(10, 6))

    cols = [tau]
    for n_0, ls, lw in [(10, "-", 0.8), (100, "-", 2.0), (1000, "--", 1.4)]:
        n_vals = n_bar(tau, n_0)
        cols.append(n_vals)
        ax.plot(tau, n_vals, color="black", ls=ls, lw=lw,
                label=rf"$\bar{{n}}_0 = {n_0}$")

    ax.axhline(y=N_STAR, color="black", ls="--", lw=0.8,
               label=r"$n^* = 0.2$ (порог)")
    ax.axhline(y=N_DOT / ETA, color="gray", ls="-.", lw=0.7,
               label=r"$\bar{n}_\infty = \dot{n}/\eta = 0.1$")
    ax.axvline(x=tau_buffer(100), color="black", ls=":", lw=1.2,
               label=r"$\tau_б \approx 0.69$ с (типовой)")

    t_q, n_q = qutip_cooling_curve(100)
    max_dev = None
    if n_q is not None:
        ax.plot(t_q, n_q, "r.", ms=5, label="QuTiP (Линдблад, независимо)")
        max_dev = float(np.max(np.abs(n_q - n_bar(t_q, 100))))
        np.savetxt("figure7_qutip.csv", np.column_stack([t_q, n_q]),
                   header="t_s,n_qutip", comments="", delimiter=",")

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"Длительность буфера $\tau$ (с)", fontsize=12)
    ax.set_ylabel(r"Среднее число фононов $\bar{n}(\tau)$", fontsize=12)
    ax.set_title("Рисунок 7: численная верификация Контура 3\n"
                 r"(параметры: $\eta = 10$ с$^{-1}$, $\dot{n} = 1$ фон/с)", fontsize=13)
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(True, which="both", ls="-", alpha=0.15)
    ax.set_xlim(0.001, 10); ax.set_ylim(0.05, 2000)

    np.savetxt("figure7_data.csv", np.column_stack(cols),
               header="tau_s,n10,n100,n1000", comments="", delimiter=",")

    plt.tight_layout()
    plt.savefig("contour3_buffer_dynamics.png", dpi=300, bbox_inches="tight")
    plt.close()
    print("✓ Рисунок 7 сохранён: contour3_buffer_dynamics.png")
    return max_dev


# ── Верификация ───────────────────────────────────────────────────────────────
def numerical_verification(max_dev):
    """Консольный отчёт + assertions (дублируются юнит-тестами)."""
    print("=" * 70)
    print("Верификация аналитической оценки τ_б ≈ 0.7 с (формула 6)")
    print("=" * 70)
    for n_0 in (10, 100, 1000):
        tau_b = tau_buffer(n_0)
        n_fin = n_bar(tau_b, n_0)
        assert abs(n_fin - N_STAR) < 1e-9, "формула (6) несовместима с (5)"
        print(f"n̄₀ = {n_0:4d} → τ_б = {tau_b:.3f} с, "
              f"n̄(τ_б) = {n_fin:.4f} (≤ n*={N_STAR})")
    assert abs(tau_buffer(100) - 0.6908) < 1e-3

    if max_dev is not None:
        print(f"Макс. отклонение QuTiP-расчёта от аналитики: {max_dev:.2e}")
        assert max_dev < 1e-4, "Линдблад-расчёт расходится с аналитикой"
    else:
        print("QuTiP не установлен: режим только аналитики (явно помечено).")
    print("=" * 70)


if __name__ == "__main__":
    print("Генерация Рисунков 6–7 для статьи TurtleShell...\n")
    generate_figure6()
    dev = generate_figure7()
    numerical_verification(dev)
    print("\n✓ Готово: contour3_buffer_duration.png, "
          "contour3_buffer_dynamics.png, figure7_data.csv")
