"""Bewertung eines ganzen Personenbestands (Aktive und Rentner)."""
import csv
from dataclasses import dataclass

from .bewertung import VERFAHREN


@dataclass
class Person:
    id: str
    status: str        # "aktiv" oder "rentner"
    geschlecht: str    # "m" oder "w"
    geburtsjahr: int
    alter: int         # versicherungstechnisches Alter am Stichtag
    eintritt: int      # Alter bei Diensteintritt
    rente: float       # (zugesagte) Jahresrente in Euro


def lade_bestand(pfad):
    """Liest einen Bestand aus einer CSV-Datei
    (Spalten: id,status,geschlecht,geburtsjahr,alter,eintritt,rente)."""
    with open(pfad, newline="", encoding="utf-8") as f:
        return [Person(r["id"], r["status"], r["geschlecht"], int(r["geburtsjahr"]), int(r["alter"]),
                       int(r["eintritt"]), float(r["rente"]))
                for r in csv.DictReader(f)]


def bewerte_bestand(tafel, bestand, verfahren, zins, z=67):
    """Rückstellung je Person und Summe für ein Bewertungsverfahren ("Teilwert" oder "PUC").

    tafel  eine Sterbetafel für alle Personen, oder eine Funktion Person -> Sterbetafel
           (z. B. um jede Person mit ihrer eigenen Kohortentafel zu bewerten).
    """
    tafel_fuer = tafel if callable(tafel) else (lambda p: tafel)
    f = VERFAHREN[verfahren]
    einzeln = {p.id: f(tafel_fuer(p), p.eintritt, p.alter, z, p.rente, zins) for p in bestand}
    return sum(einzeln.values()), einzeln
