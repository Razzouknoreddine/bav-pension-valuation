"""Bewertungsverfahren: Randwerte, Monotonie, Verhältnis Teilwert zu PUC."""
import pytest

from bavpension import Sterbetafel, duration, leistungsbarwert, puc, teilwert

T = Sterbetafel()
E, Z, R = 30, 67, 6000


@pytest.mark.parametrize("verfahren", [teilwert, puc])
def test_rueckstellung_bei_eintritt_null(verfahren):
    assert verfahren(T, E, E, Z, R, 0.03) == pytest.approx(0.0, abs=1e-8)


@pytest.mark.parametrize("verfahren", [teilwert, puc])
def test_bei_rentenbeginn_gleich_leistungsbarwert(verfahren):
    assert verfahren(T, E, Z, Z, R, 0.03) == pytest.approx(leistungsbarwert(T, Z, Z, R, 0.03))


@pytest.mark.parametrize("verfahren", [teilwert, puc])
def test_rueckstellung_steigt_mit_dienstzeit(verfahren):
    werte = [verfahren(T, E, x, Z, R, 0.03) for x in range(E, Z + 1)]
    assert all(a < b for a, b in zip(werte, werte[1:]))


def test_hoeherer_zins_senkt_rueckstellung():
    assert puc(T, E, 45, Z, R, 0.03) < puc(T, E, 45, Z, R, 0.02)


def test_steuerwert_unter_hgb_wert():
    # Steuerbilanz (Teilwert, 6 %) liegt unter Handelsbilanz (PUC, ~2 %)
    assert teilwert(T, E, 45, Z, R, 0.06) < puc(T, E, 45, Z, R, 0.0219)


def test_duration_naeherung():
    # Δ V / V  ≈  -D/(1+i) * Δi  für eine kleine Zinsänderung
    x, i, di = 45, 0.02, 0.0001
    v0, v1 = puc(T, E, x, Z, R, i), puc(T, E, x, Z, R, i + di)
    assert (v1 - v0) / v0 == pytest.approx(-duration(T, x, Z, i) / (1 + i) * di, rel=0.01)
