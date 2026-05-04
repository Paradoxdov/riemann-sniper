# 🎯 riemann-sniper

A Python library for fast and accurate root-finding of the Riemann zeta function zeros on the critical line $s = 1/2 + it$. 

Instead of full-line scanning, the algorithm instantly calculates the approximate position of the zero using the inverse Lambert W function and Gram points, and then localizes it with high precision.

---

## 🛠 Installation

```bash
pip install riemann-sniper
```

---

## 📖 Usage Guide

The library supports two modes: fast (for lower heights) and ultra-precise (for trillionth orders).

### 1. Standard Request (Fast Mode)
Ideal for zeros up to the order of $10^9$. Uses standard Python precision (`float64`).

```python
from riemann_sniper import RiemannZeroFinder

# Initialize the finder
finder = RiemannZeroFinder()

# Set the ordinal number of the zero
n = 10**6

# Find the height t
t = finder.find_nth_zero(n)

# IMPORTANT: Use curly braces inside the f-string when printing!
print(f"Height of the {n}-th zero: {t:.8f}")
# Expected output: 600269.67701244
```

### 2. Ultra-Precise Request (For zeros of order $10^{12}$ and above)
At massive heights, zeros are located very densely (step $\approx 0.25$). Due to the rounding noise of standard `float64`, the algorithm might capture a neighboring zero. 
For a correct query, **you must increase the computation precision** using the `mpmath` library.

```python
from mpmath import mp
from riemann_sniper import RiemannZeroFinder

# 1. Enable high precision (30-50 decimal places) BEFORE running the search
mp.dps = 30 

finder = RiemannZeroFinder()

# 2. Find the trillionth zero. 
# Warning: due to O(sqrt(T)) complexity, computation on 1 core will take 3 to 20 minutes!
n_huge = 10**12
t_huge = finder.find_nth_zero(n_huge)

print(f"Trillionth zero: {t_huge:.8f}")
```

---

## 📊 Performance & Benchmarks

Tests were run on a standard desktop CPU (single-threaded mode):

| Zero Order ($n$) | Height ($t$) | Time | Precision Requirements |
| :--- | :--- | :--- | :--- |
| **$10^6$** | $\approx 6 \times 10^5$ | **Instant** | Standard `float64` |
| **$10^9$** | $\approx 3.7 \times 10^8$ | **~1.5 sec** | Matches Odlyzko datasets |
| **$32\,132\,336\,741$** | $\approx 1.3 \times 10^{10}$ | **~7.0 sec** | Base precision up to 6th decimal place |
| **$10^{12}$** | $\approx 2.6 \times 10^{11}$ | **3 - 20 min** | **Strictly requires `mp.dps >= 30`** |

- **Complexity:** Computations follow $O(\sqrt{T})$ due to the Riemann-Siegel formula summation.
- **Prediction Error ($L_0$):** $\approx 0.043$ (thanks to the Lambert $W$ function approximation).

---

## ⚠️ Troubleshooting

1. **Console prints code instead of a number:** If you write `print(f"finder.find_nth_zero(10**6):.8f")`, Python will output this string as text. Be sure to wrap the function call in **curly braces**: `print(f"{finder.find_nth_zero(10**6):.8f}")`.
2. **Program "hangs":** Finding zeros above $10^{10}$ requires summing hundreds of thousands of terms. The program hasn't crashed — it's loading the CPU at 100%. Please wait for it to finish.
3. **Result deviates from reference tables:** If your result differs from Gourdon's tables by $\approx 0.22 - 0.25$, it means a neighboring zero was found due to insufficient precision. Solution: increase `mp.dps` to 30 or 50.

---

## ⚙️ Requirements

The following dependencies are required:
* Python 3.7+
* `numpy`
* `scipy`
* `mpmath` (Crucially important for arbitrary-precision arithmetic at heights > $10^9$)

---

## 🤝 Contributing

The project is in early access. We particularly welcome Pull Requests in the following areas:
1. **Optimization:** Porting the Riemann-Siegel summation to C, Cython, or Numba to break the performance barrier of pure Python.
2. **Batch Processing:** Functions for finding arrays of zeros within a given range (interval scanning).

## ⚖️ License
Distributed under the **MIT License**.
