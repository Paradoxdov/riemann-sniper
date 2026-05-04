import numpy as np
import mpmath
from scipy.optimize import brentq
from scipy.special import lambertw

# Устанавливаем точность mpmath
mpmath.mp.dps = 15

class RiemannZeroFinder:
    def __init__(self):
        self.TWO_PI = 2.0 * np.pi

    def predict_level_0(self, n: int) -> float:
        n_shifted = float(n) - 0.5
        z = (n_shifted - 7.0/8.0) / np.e
        w = np.real(lambertw(z, k=0))
        return self.TWO_PI * (n_shifted - 7.0/8.0) / w

    def Z(self, t: float) -> float:
        return float(mpmath.siegelz(t))

    def theta(self, t: float) -> float:
        return float(mpmath.siegeltheta(t))

    def nzeros(self, t: float) -> int:
        return int(mpmath.nzeros(t))

    def gram_point(self, k: int) -> float:
        target = k * np.pi
        w = np.real(lambertw((target + np.pi / 8.0) / (np.e * np.pi)))
        t = self.TWO_PI * np.e * np.exp(w)
        for _ in range(4):
            th = self.theta(t)
            dth = 0.5 * np.log(t / self.TWO_PI)
            t -= (th - target) / dth
        return t

    def _grid_sign_changes(self, a: float, b: float, n_grid: int) -> list:
        ts = np.linspace(a, b, n_grid)
        zs = np.array([self.Z(t) for t in ts])
        return [(ts[i], ts[i+1]) for i in range(len(zs)-1) if zs[i] * zs[i+1] < 0]

    def find_zeros_in_interval(self, g_left: float, g_right: float, expected_count: int, grid_pts: int = 400) -> list:
        if expected_count == 0:
            return []
        if expected_count == 1:
            z_l, z_r = self.Z(g_left), self.Z(g_right)
            if z_l * z_r < 0:
                return [brentq(self.Z, g_left, g_right, xtol=1e-12)]
            brackets = self._grid_sign_changes(g_left, g_right, 60)
            if brackets:
                return [brentq(self.Z, *brackets[0])]
            return [np.nan]

        brackets = self._grid_sign_changes(g_left, g_right, grid_pts)
        if len(brackets) >= expected_count:
            return sorted([brentq(self.Z, a, b) for a, b in brackets[:expected_count]])
        if grid_pts < 3200:
            return self.find_zeros_in_interval(g_left, g_right, expected_count, grid_pts * 2)
            
        t_mid = (g_left + g_right) / 2.0
        n_left = self.nzeros(t_mid) - self.nzeros(g_left)
        z1 = self.find_zeros_in_interval(g_left, t_mid, n_left, 400)
        z2 = self.find_zeros_in_interval(t_mid, g_right, expected_count - n_left, 400)
        return sorted(z1 + z2)

    def find_nth_zero(self, n: int) -> float:
        t_pred = self.predict_level_0(n)
        k_est = int(self.theta(t_pred) / np.pi)
        
        g_current = self.gram_point(k_est)
        N_current = self.nzeros(g_current)
        
        if N_current < n:
            g_left, N_left = g_current, N_current
            k = k_est + 1
            while True:
                g_right = self.gram_point(k)
                N_right = self.nzeros(g_right)
                if N_right >= n:
                    break
                g_left, N_left = g_right, N_right
                k += 1
        else:
            g_right, N_right = g_current, N_current
            k = k_est - 1
            while True:
                g_left = self.gram_point(k)
                N_left = self.nzeros(g_left)
                if N_left < n:
                    break
                g_right, N_right = g_left, N_left
                k -= 1

        expected_zeros = N_right - N_left
        zeros_in_interval = self.find_zeros_in_interval(g_left, g_right, expected_zeros)
        
        local_idx = n - N_left - 1
        if 0 <= local_idx < len(zeros_in_interval):
            return zeros_in_interval[local_idx]
        else:
            raise ValueError(f"Нуль не найден локально! N_left={N_left}, N_right={N_right}")