"""Plausibilität der Sterbetafel."""
from bavpension import MAX_ALTER, Sterbetafel

T = Sterbetafel()


def test_wahrscheinlichkeiten_im_intervall():
    assert all(0.0 <= T.qx(x) <= 1.0 for x in range(MAX_ALTER + 1))
    assert T.qx(MAX_ALTER) == 1.0


def test_sterblichkeit_steigt_ab_30():
    assert all(T.qx(x) < T.qx(x + 1) for x in range(30, MAX_ALTER))


def test_ueberleben_multiplikativ():
    # (s+t)_p_x = s_p_x * t_p_{x+s}
    assert abs(T.tpx(40, 30) - T.tpx(40, 10) * T.tpx(50, 20)) < 1e-12


def test_lebenserwartung_mit_67_plausibel():
    assert 17 < T.lebenserwartung(67) < 22
