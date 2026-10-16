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

    # substitute upward
    for i in range(n - 3, -1, -1):
        ai, qi, bi, ri = steps[i]
        # current expression: cA*(bi) + cB*(ri), and ri = ai - qi*bi
        lines.append(
            f"   = {cA}({bi}) + ({cB})[{ai} - {qi}({bi})]      (replace {ri})"
        )
        newA = cB
        newB = cA - cB * qi
        lines.append(f"   = {expr(newA, ai, newB, bi)}")
        cA, cB = newA, newB

    return lines, cA, cB


# -------------------------------------------------------------------- app
st.set_page_config(page_title="Diophantine Solver", page_icon="🧮")
st.title("🧮 Linear Diophantine Equation Solver")
st.caption("Solves  ax + by = c  step by step (Euclid + Extended Euclid)")

col1, col2, col3 = st.columns(3)
a = col1.number_input("a", value=172, step=1)
b = col2.number_input("b", value=20, step=1)
c = col3.number_input("c", value=1000, step=1)
a, b, c = int(a), int(b), int(c)

st.latex(rf"{a}x + {b}y = {c}")

if a == 0 or b == 0:
    st.error("Please use non-zero values for a and b.")
    st.stop()

# ---------------------------------------------------------------- STEP 1
st.header("Step 1: Find the GCD")
steps1, g = euclid_steps(abs(a), abs(b))
st.code("\n".join(f"{x} = {q}({y}) + {r}" for x, q, y, r in steps1))
st.success(f"gcd({a}, {b}) = {g}")

# ---------------------------------------------------------------- STEP 2
st.header("Step 2: Check if the GCD divides the given c")
if c % g != 0:
    st.latex(rf"{g} \nmid {c}")
    st.error(f"{g} does not divide {c}, so there is **no integer solution**.")
    st.stop()
st.latex(rf"{g} \mid {c} \;\Rightarrow\; \frac{{{c}}}{{{g}}} = {c // g}")
st.success("Yes, there is an integer solution.")

# ---------------------------------------------------------------- STEP 3
st.header("Step 3: Simplify")
a1, b1, c1 = a // g, b // g, c // g
st.latex(
    rf"\frac{{{a}x + {b}y}}{{{g}}} = \frac{{{c}}}{{{g}}}"
    rf"\;\Rightarrow\; {a1}x + {b1}y = {c1}"
)

# ---------------------------------------------------------------- STEP 4
st.header("Step 4: Use the Extended Euclidean Algorithm")
steps4, g4 = euclid_steps(abs(a1), abs(b1))
st.code("\n".join(f"{x} = {q}({y}) + {r}" for x, q, y, r in steps4))
st.success(f"gcd({a1}, {b1}) = {g4}")

# ---------------------------------------------------------------- STEP 5
st.header("Step 5: Back-substitute to simplify")
lines, u, v = back_substitute(steps4)
st.code("\n".join(lines))

A, B = abs(a1), abs(b1)
st.write(f"So:  1 = {expr(u, A, v, B)}")
assert u * A + v * B == 1

st.write(f"Multiply both sides by {c1}:")
st.code(f"{c1}  =  {u * c1}({A}) + ({v * c1})({B})")

# fix signs if a or b were negative
sa = 1 if a1 > 0 else -1
sb = 1 if b1 > 0 else -1
x0, y0 = u * c1 * sa, v * c1 * sb
if sa < 0 or sb < 0:
    st.info("a or b is negative, so the signs of x₀ and y₀ were adjusted.")

st.subheader("Particular solution")
st.latex(rf"x_0 = {x0}, \quad y_0 = {y0}")

st.subheader("General solution")
st.latex(
    r"x = x_0 + \left(\frac{b}{d}\right)t \qquad "
    r"y = y_0 - \left(\frac{a}{d}\right)t"
)
# d = 1 for the simplified equation
st.latex(rf"x = {x0} + {b1}t \qquad y = {y0} - {a1}t")


def signed(const, coef, var="t"):
    sign = "+" if coef >= 0 else "-"
    return f"{const} {sign} {abs(coef)}{var}"


fx = signed(x0, b1)
fy = signed(y0, -a1)
st.success(f"**x = {fx}**     and     **y = {fy}**     (t is any integer)")

# ----------------------------------------------------------- verification
st.header("✅ Check")
t_min, t_max = st.slider("Range of t to display", -10, 10, (-3, 3))
rows = []
for t in range(t_min, t_max + 1):
    x = x0 + b1 * t
    y = y0 - a1 * t
    rows.append(
        {"t": t, "x": x, "y": y, f"{a}x + {b}y": a * x + b * y, "= c ?": a * x + b * y == c}
    )
st.dataframe(rows, use_container_width=True, hide_index=True)
