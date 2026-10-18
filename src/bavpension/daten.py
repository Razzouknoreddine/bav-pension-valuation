"""Echte Rechnungsgrundlagen: Destatis-Kohortensterbetafeln und Bundesbank-Rechnungszins.

Quellen (Weitergabe mit Quellenangabe gestattet):
  - Statistisches Bundesamt (Destatis), Statistischer Bericht
    "Kohortensterbetafeln für Deutschland 1926-2026", erschienen 16.09.2026, EVAS 12621
  - Deutsche Bundesbank, Abzinsungszinssätze gemäß § 253 Abs. 2 HGB, 10-Jahresdurchschnitt
"""
import csv
from functools import lru_cache
from pathlib import Path

from .sterbetafel import MAX_ALTER, Sterbetafel

DATEN = Path(__file__).resolve().parents[2] / "data"
VARIANTEN = {1: "niedrig", 2: "mittel", 3: "hoch"}   # Annahme zum Anstieg der Lebenserwartung


@lru_cache(maxsize=None)
def _alle_kohorten():
    tafeln = {}
    with open(DATEN / "destatis_kohortensterbetafeln.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            schluessel = (int(r["jahrgang"]), r["geschlecht"], int(r["variante"]))
            tafeln.setdefault(schluessel, {})[int(r["alter"])] = float(r["qx"])
    return tafeln


class KohortenSterbetafel(Sterbetafel):
    """Sterbetafel eines Geburtsjahrgangs (Generationentafel) nach Destatis.

    jahrgang    Geburtsjahr 1926 ... 2026
    geschlecht  "m" oder "w"
    variante    1 = niedriger, 2 = mittlerer, 3 = hoher Anstieg der Lebenserwartung

    q_x ist die Sterbewahrscheinlichkeit dieses Jahrgangs im Alter x, also im Kalenderjahr
    jahrgang + x. Die Tafel folgt damit der Diagonale einer Periodentafel.
    """

    def __init__(self, jahrgang, geschlecht="m", variante=2):
        try:
            qx = _alle_kohorten()[(jahrgang, geschlecht, variante)]
        except KeyError:
            raise ValueError(f"Keine Tafel für Jahrgang {jahrgang}, Geschlecht {geschlecht!r}, Variante {variante}")
        self.jahrgang, self.geschlecht, self.variante = jahrgang, geschlecht, variante
        # Destatis endet mit "100 und mehr" (q = 1); darüber lebt niemand
        self.q = [qx.get(x, 1.0) for x in range(MAX_ALTER + 1)]

    def __repr__(self):
        return f"KohortenSterbetafel({self.jahrgang}, {self.geschlecht!r}, Variante {self.variante})"


@lru_cache(maxsize=None)
def _zinsreihe():
    with open(DATEN / "bundesbank_hgb_zins_10j.csv", encoding="utf-8") as f:
        return {r["stichtag"]: {int(k[1:]): float(v) / 100 for k, v in r.items() if k != "stichtag"}
                for r in csv.DictReader(f)}


def stichtage():
    """Alle verfügbaren Monatsenden (ISO-Datum), aufsteigend."""
    return sorted(_zinsreihe())


def hgb_zins(stichtag=None, restlaufzeit=15):
    """HGB-Rechnungszins (10-Jahres-Durchschnitt) als Dezimalzahl.

    stichtag      "JJJJ-MM-TT" (Monatsende); None = letzter verfügbarer Wert
    restlaufzeit  1 ... 50 Jahre; 15 = Vereinfachungsregel nach § 253 Abs. 2 Satz 2 HGB
    """
    reihe = _zinsreihe()
    return reihe[stichtag or max(reihe)][restlaufzeit]
