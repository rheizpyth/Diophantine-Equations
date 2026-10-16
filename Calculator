import streamlit as st


# ---------------------------------------------------------------- helpers
def euclid_steps(a, b):
    """Return list of (a, q, b, r) with a = q*b + r, and the gcd."""
    steps = []
    while b != 0:
        q, r = divmod(a, b)
        steps.append((a, q, b, r))
        a, b = b, r
    return steps, a


def expr(c1, x1, c2, x2):
    """Format  c1(x1) + c2(x2)  with proper signs."""
    s = f"{c1}({x1})"
    s += f" + {c2}({x2})" if c2 >= 0 else f" - {abs(c2)}({x2})"
    return s


def back_substitute(steps):
    """
    Back-substitute through the Euclid steps.
    Returns (lines, u, v) such that gcd = u*a0 + v*b0.
    """
    n = len(steps)
    lines = []

    if n == 1:  # b divides a exactly
        a, q, b, r = steps[0]
        lines.append(f"{b} divides {a} exactly, so gcd = {b} = 0({a}) + 1({b})")
        return lines, 0, 1

    # last equation with a non-zero remainder:  g = a - q(b)
    a, q, b, r = steps[n - 2]
    cA, cB = 1, -q
    lines.append(f"{r} = {a} - {q}({b})")
