"""Sterbetafel nach dem Gompertz-Makeham-Gesetz.

In der Praxis werden in Deutschland die Heubeck-Richttafeln verwendet. Sie sind
lizenzpflichtig, deshalb wird hier eine parametrische Tafel benutzt:

    Sterbeintensität      mu(x) = A + B * c^x
    einjährige Sterbewahrscheinlichkeit
                          q_x = 1 - exp( -Integral_x^{x+1} mu(s) ds )
"""
import math

MAX_ALTER = 120  # Schlussalter omega


class Sterbetafel:
    """Einjährige Sterbewahrscheinlichkeiten q_x für x = 0, ..., MAX_ALTER."""

    def __init__(self, A=0.00022, B=0.0000150, c=1.1035):
        self.A, self.B, self.c = A, B, c
        self.q = []
        for x in range(MAX_ALTER + 1):
            integral = A + B * c**x * (c - 1) / math.log(c)
            self.q.append(1 - math.exp(-integral))
        self.q[MAX_ALTER] = 1.0  # niemand überlebt das Schlussalter

    def qx(self, x):
        """Wahrscheinlichkeit, dass ein x-Jähriger innerhalb eines Jahres stirbt."""
        return 1.0 if x >= MAX_ALTER else self.q[x]

    def tpx(self, x, t):
        """t_p_x: Wahrscheinlichkeit, dass ein x-Jähriger noch t Jahre lebt."""
        p = 1.0
        for k in range(t):
            p *= 1 - self.qx(x + k)
            if p == 0.0:
                break
        return p

    def lebenserwartung(self, x):
        """Gestutzte Restlebenserwartung e_x = Summe_{t>=1} t_p_x (+0,5 Korrektur)."""
        return sum(self.tpx(x, t) for t in range(1, MAX_ALTER - x + 1)) + 0.5
