import pytest
from contour3_verification import n_bar, tau_buffer, N_STAR, TAU_B_EXACT


def test_tau_buffer_typical():
    assert abs(tau_buffer(100) - TAU_B_EXACT) < 1e-9


def test_tau_buffer_monotonic_in_n0():
    assert tau_buffer(10) < tau_buffer(100) < tau_buffer(1000)


def test_threshold_reached_exactly():
    for n_0 in (10, 100, 1000):
        assert abs(n_bar(tau_buffer(n_0), n_0) - N_STAR) < 1e-9


def test_unreachable_threshold_raises():
    with pytest.raises(ValueError):
        tau_buffer(100, n_dot=2.0)   # n_inf = 0.2 = n* → буфер невозможен
