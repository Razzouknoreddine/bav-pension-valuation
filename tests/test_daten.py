"""Echte Daten: Destatis-Kohortentafeln und Bundesbank-Zins."""
import pytest

from bavpension import KohortenSterbetafel, hgb_zins, leibrente, puc, stichtage


def test_kohortentafel_wahrscheinlichkeiten():
    t = KohortenSterbetafel(1981, "m", 2)
    assert all(0.0 <= t.qx(x) <= 1.0 for x in range(121))
    assert t.qx(100) == 1.0               # "100 und mehr"


def test_frauen_leben_laenger():
    assert KohortenSterbetafel(1981, "w", 2).lebenserwartung(67) > KohortenSterbetafel(1981, "m", 2).lebenserwartung(67)


def test_varianten_geordnet():
    # Variante 1/2/3 = niedriger/mittlerer/hoher Anstieg der Lebenserwartung
    e = [KohortenSterbetafel(1981, "m", v).lebenserwartung(67) for v in (1, 2, 3)]
    assert e[0] < e[1] < e[2]


def test_juengerer_jahrgang_lebt_laenger():
    # Kohorteneffekt: steigende Lebenserwartung
    assert KohortenSterbetafel(1991, "m", 2).lebenserwartung(67) > KohortenSterbetafel(1961, "m", 2).lebenserwartung(67)


def test_langlebigkeit_erhoeht_rueckstellung():
    v1 = puc(KohortenSterbetafel(1981, "m", 1), 30, 45, 67, 6000, 0.0225)
    v3 = puc(KohortenSterbetafel(1981, "m", 3), 30, 45, 67, 6000, 0.0225)
    assert v3 > v1


def test_unbekannter_jahrgang():
    with pytest.raises(ValueError):
        KohortenSterbetafel(1900, "m", 2)


def test_bundesbank_bekannte_werte():
    # veröffentlichte Werte für 15 Jahre Restlaufzeit
    assert hgb_zins("2025-12-31") == pytest.approx(0.0206)
    assert hgb_zins("2024-12-31") == pytest.approx(0.0190)
    assert stichtage()[0] == "2015-01-31"
    assert hgb_zins() == hgb_zins(stichtage()[-1])
