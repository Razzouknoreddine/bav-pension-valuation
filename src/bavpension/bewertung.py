"""Bewertungsverfahren für Pensionsrückstellungen (DAV-Leitfaden, Kap. 5.4).

e  Alter bei Diensteintritt
x  Alter am Bewertungsstichtag
z  Pensionierungsalter
"""
from .barwerte import leistungsbarwert, temporaere_leibrente


def teilwert(tafel, e, x, z, rente, zins):
    """Teilwertverfahren (Pflicht in der Steuerbilanz, § 6a EStG).

    Fiktive gleichbleibende Prämie ab Diensteintritt:
        P = B^L_e / ä_{e:z-e}
    Teilwert = Leistungsbarwert minus Barwert der noch ausstehenden Prämien:
        V = B^L_x - P * ä_{x:z-x}
    """
    if x >= z:
        return leistungsbarwert(tafel, x, z, rente, zins)
    P = leistungsbarwert(tafel, e, z, rente, zins) / temporaere_leibrente(tafel, e, z - e, zins)
    return leistungsbarwert(tafel, x, z, rente, zins) - P * temporaere_leibrente(tafel, x, z - x, zins)


def puc(tafel, e, x, z, rente, zins):
    """Projected-Unit-Credit-Methode (IFRS / IAS 19, üblich im HGB).

    Der Anspruch wird proportional zur Dienstzeit erdient:
        V = (x - e) / (z - e) * B^L_x
    """
    if x >= z:
        return leistungsbarwert(tafel, x, z, rente, zins)
    return (x - e) / (z - e) * leistungsbarwert(tafel, x, z, rente, zins)


VERFAHREN = {"Teilwert": teilwert, "PUC": puc}
