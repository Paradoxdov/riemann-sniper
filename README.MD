## 📊 Performance & Benchmarks

The library is designed for both rapid exploration and deep-sea mathematical hunting. Below are the typical benchmarks on a standard consumer-grade CPU (single thread):

| Order ($n$) | Height ($t$) | Time | Precision Note |
| :--- | :--- | :--- | :--- |
| **$10^6$** | $\approx 6 \times 10^5$ | **Instant** | Perfect for visualization |
| **$10^9$** | $\approx 3.7 \times 10^8$ | **~1.5 seconds** | Matches Odlyzko datasets |
| **$32,132,336,741$** | $\approx 1.3 \times 10^{10}$ | **~7.0 seconds** | High-speed Python execution |
| **$10^{12}$** | $\approx 2.6 \times 10^{11}$ | **~3-20 minutes** | Requires `mp.dps >= 30` |

### Key Metrics (at 32B scale):
* **Prediction Error ($L_0$):** ~0.043 (Thanks to Lambert W approximation).
* **Accuracy:** Matches Odlyzko/Platt datasets up to the 6th decimal place with standard `float64`.
* **Complexity:** Computation follows $O(\sqrt{T})$ due to the Riemann-Siegel summation.

---

## 🛠 Requirements

To maintain high precision while staying lightweight, we rely on:
* **Python 3.7+**
* **NumPy & SciPy**
* **mpmath** (crucial for heights above $10^9$)

---

## ⚖️ License

Distributed under the **MIT License**. You are free to use it for research, education, or even for claiming the Million Dollar Prize (just don't forget us in the credits!).

---

## 🤝 Contributing

We are in the "early access" phase of hunting the biggest zeros. We particularly welcome contributions in:
* **Optimization:** Implementing Riemann-Siegel in C or via `Numba`.
* **Batch Processing:** Functions to find ranges of zeros at once.
* **UI/UX:** Better visualization tools for the critical line.

Feel free to open an **Issue** or submit a **Pull Request**!
