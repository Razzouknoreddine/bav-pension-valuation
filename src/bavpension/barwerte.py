"""Barwerte der Pensionsversicherungsmathematik (DAV-Leitfaden, Kap. 4.2 und 5.3).

Notation:  v = 1/(1+i) Diskontfaktor,  t_p_x Überlebenswahrscheinlichkeit.
Alle Renten sind jährlich vorschüssig mit dem Jahresbetrag 1.
"""
from .sterbetafel import MAX_ALTER


def diskont(zins):
    return 1.0 / (1.0 + zins)


def leibrente(tafel, x, zins):
    """ä_x = Summe_{k>=0} v^k * k_p_x   (lebenslange Rente ab sofort)."""
    v = diskont(zins)
    return sum(v**k * tafel.tpx(x, k) for k in range(MAX_ALTER - x + 1))


def temporaere_leibrente(tafel, x, n, zins):
    """ä_{x:n} = Summe_{k=0}^{n-1} v^k * k_p_x   (höchstens n Zahlungen)."""
    v = diskont(zins)
    return sum(v**k * tafel.tpx(x, k) for k in range(n))


def aufgeschobene_leibrente(tafel, x, n, zins):
    """n|ä_x = v^n * n_p_x * ä_{x+n}   (Rente beginnt erst in n Jahren)."""
    return diskont(zins)**n * tafel.tpx(x, n) * leibrente(tafel, x + n, zins)


def leistungsbarwert(tafel, x, z, rente, zins):
    """B^L_x: Barwert einer Altersrente `rente` ab Alter z für einen x-jährigen Aktiven.

    Vor Rentenbeginn: aufgeschobene Leibrente.  Ab Rentenbeginn: laufende Leibrente.
    """
    if x >= z:
        return rente * leibrente(tafel, x, zins)
    return rente * aufgeschobene_leibrente(tafel, x, z - x, zins)


def erwartete_zahlungen(tafel, x, z, rente):
    """Erwartete Rentenzahlungen CF_t = rente * t_p_x für t = 0, 1, 2, ... (ab Alter z)."""
    start = max(z - x, 0)
    return {t: rente * tafel.tpx(x, t) for t in range(start, MAX_ALTER - x + 1)}


def duration(tafel, x, z, zins):
    """Macaulay-Duration der Verpflichtung: zinsgewichtete mittlere Laufzeit in Jahren.

    D = Summe t * v^t * CF_t / Summe v^t * CF_t.
    Näherung:  relative Änderung der Rückstellung  ~  -D / (1+i) * Zinsänderung.
    """
    v = diskont(zins)
    cf = erwartete_zahlungen(tafel, x, z, 1.0)
    pv = sum(v**t * c for t, c in cf.items())
    return sum(t * v**t * c for t, c in cf.items()) / pv
