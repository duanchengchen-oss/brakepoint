"""
edistance_core.py — dependency-light core for perturbation effect sizes.

Pure-numpy E-distance (energy distance) + permutation E-test, with a
self-contained synthetic smoke test. Runs anywhere numpy is installed —
no scanpy/pertpy — so the core statistic is unit-testable independently of
the heavy single-cell stack it will run inside (Claude Science / your env).

E-distance (Peidli et al., scPerturb, Nat Methods 2024), squared-Euclidean form:
    E(X,Y) = 2*mean||x_i - y_j||^2 - mean||x_i - x_k||^2 - mean||y_j - y_l||^2
           = 2*sigma_XY - sigma_XX - sigma_YY   (>= 0; larger = bigger effect)

Design notes baked in from the red-team:
- Rank perturbations by E-distance MAGNITUDE; use the permutation p only as a gate
  (significance scales with cell count, not biology).
- power_equalize() subsamples groups to a common n so E-distance is comparable
  across perturbations with different coverage.
"""
import numpy as np


def _sum_sq_pairwise(A: np.ndarray, B: np.ndarray) -> float:
    """Sum over all pairs of squared Euclidean distance via the ||a-b||^2 identity."""
    aa = (A * A).sum(1)[:, None]
    bb = (B * B).sum(1)[None, :]
    d2 = aa + bb - 2.0 * (A @ B.T)
    np.maximum(d2, 0.0, out=d2)
    return float(d2.sum())


def e_distance(X: np.ndarray, Y: np.ndarray) -> float:
    """Energy distance (squared-Euclidean form), unbiased U-statistic.

    The two within-group terms EXCLUDE the zero self-distance diagonal (divide by
    n(n-1), not n^2). Including it is a V-statistic bias that shrinks the within terms
    and inflates E by ~(sXX+sYY)/n ~= 4d/n for unit-covariance Gaussians in d dims —
    an n-dependent offset that corrupts the cross-perturbation magnitude ranking.
    """
    n_x, n_y = len(X), len(Y)
    s_xy = _sum_sq_pairwise(X, Y) / (n_x * n_y)
    s_xx = _sum_sq_pairwise(X, X) / (n_x * (n_x - 1))     # off-diagonal (diagonal is 0)
    s_yy = _sum_sq_pairwise(Y, Y) / (n_y * (n_y - 1))
    return 2.0 * s_xy - s_xx - s_yy


def power_equalize(X, Y, seed=0):
    """Subsample the larger group so both have n = min(len(X), len(Y)) cells."""
    rng = np.random.default_rng(seed)
    n = min(len(X), len(Y))
    xi = rng.choice(len(X), n, replace=False)
    yi = rng.choice(len(Y), n, replace=False)
    return X[xi], Y[yi]


def e_test(X, Y, n_perm=1000, seed=0, equalize=True):
    """Permutation E-test. Returns (E_distance, p_value). p is one-sided (E >= observed)."""
    if equalize:
        X, Y = power_equalize(X, Y, seed=seed)
    rng = np.random.default_rng(seed)
    obs = e_distance(X, Y)
    Z = np.vstack([X, Y])
    nX = len(X)
    count = 0
    for _ in range(n_perm):
        idx = rng.permutation(len(Z))
        if e_distance(Z[idx[:nX]], Z[idx[nX:]]) >= obs:
            count += 1
    return obs, (count + 1) / (n_perm + 1)


def _smoke() -> None:
    rng = np.random.default_rng(42)
    d = 50

    # (1) Regression guard for the diagonal-bias bug: a NULL (control vs control) must
    #     score E ~= 0 and be n-INVARIANT. Before the fix it scored ~= 4d/n (~5.0 at
    #     n=40), which let a pure-null small perturbation outrank a real effect.
    for n in (40, 500):
        a = rng.normal(0, 1, (n, d))
        b = rng.normal(0, 1, (n, d))
        e_null_n = e_distance(a, b)
        print(f"null n={n:4d}: E={e_null_n:8.4f}")
        assert abs(e_null_n) < 1.0, f"null E not ~0 at n={n} (diagonal-bias regression)"

    # (2) A real mean-shift must be recovered, dwarf the null, and be significant.
    ctrl = rng.normal(0, 1, (400, d))
    shift = np.zeros(d)
    shift[:10] = 1.5
    pert = rng.normal(0, 1, (400, d)) + shift
    e_null, p_null = e_test(ctrl, rng.normal(0, 1, (400, d)), n_perm=500, seed=1)
    e_eff, p_eff = e_test(pert, ctrl, n_perm=500, seed=1)
    # For unit-cov Gaussians shifted by mu, E-distance (squared form) = 2*||mu||^2.
    print(f"effect: E={e_eff:8.4f} p={p_eff:.4f}  "
          f"(expected E ~= 2*||shift||^2 = {2 * float((shift * shift).sum()):.1f})")
    assert e_eff > 10 * abs(e_null), "effect should dwarf the null"
    assert p_eff < 0.01, "a real effect should be significant"
    assert p_null > 0.05, "the null should be non-significant"
    print("SMOKE TEST PASSED  (E-distance unbiased + permutation E-test correct)")


if __name__ == "__main__":
    _smoke()
