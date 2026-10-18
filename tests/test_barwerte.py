"""Barwerte gegen bekannte Identitäten und Grenzfälle."""
import pytest

from bavpension import (Sterbetafel, aufgeschobene_leibrente, duration, leibrente,
                        temporaere_leibrente)

T = Sterbetafel()


def test_ohne_zins_ist_leibrente_lebenserwartung():
    # ä_x bei i = 0 ist die erwartete Anzahl Zahlungen = 1 + gestutzte Lebenserwartung
    assert leibrente(T, 67, 0.0) == pytest.approx(T.lebenserwartung(67) + 0.5)


def test_zerlegung_leibrente():
    # ä_x = ä_{x:n} + n|ä_x  (sofortige Rente = temporärer + aufgeschobener Teil)
    for x, n, i in [(45, 22, 0.02), (30, 37, 0.06), (60, 5, 0.03)]:
        assert leibrente(T, x, i) == pytest.approx(
            temporaere_leibrente(T, x, n, i) + aufgeschobene_leibrente(T, x, n, i))


def test_leibrente_faellt_mit_zins():
    assert leibrente(T, 67, 0.03) < leibrente(T, 67, 0.02) < leibrente(T, 67, 0.01)


def test_ohne_sterblichkeit_ist_zeitrente():
    # mit q = 0 wird ä_{x:n} zur sicheren Zeitrente (1 - v^n) / (1 - v)
    tafel = Sterbetafel(A=0.0, B=0.0, c=1.1)
    i, n = 0.02, 10
    v = 1 / (1 + i)
    assert temporaere_leibrente(tafel, 40, n, i) == pytest.approx((1 - v**n) / (1 - v))


def test_duration_aktiver_laenger_als_rentner():
    assert duration(T, 30, 67, 0.02) > duration(T, 70, 67, 0.02) > 0
