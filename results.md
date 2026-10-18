# Ergebnisse

Erzeugt von `scripts/run_experiments.py`.

Stichtag 2026-09-30, HGB-Zins (15 Jahre) 2,25 %, Steuerzins 6 %, Destatis-Kohortentafeln Variante 2.

## 1. Sterbetafeln

Restlebenserwartung mit 67 und Rentenbarwertfaktor ä₆₇ (HGB-Zins):

| Tafel | Lebenserwartung e₆₇ | Rentenbarwertfaktor ä₆₇ |
|---|---|---|
| Gompertz-Makeham (Modell) | 19,5 Jahre | 15,73 |
| Destatis Jahrgang 1981, Mann, Variante 1 | 17,5 Jahre | 14,49 |
| Destatis Jahrgang 1981, Mann, Variante 2 | 18,7 Jahre | 15,29 |
| Destatis Jahrgang 1981, Mann, Variante 3 | 20,1 Jahre | 16,20 |
| Destatis Jahrgang 1981, Frau, Variante 1 | 20,7 Jahre | 16,54 |
| Destatis Jahrgang 1981, Frau, Variante 2 | 21,8 Jahre | 17,28 |
| Destatis Jahrgang 1981, Frau, Variante 3 | 23,1 Jahre | 18,11 |

## 2. Einzelbewertung

Mann, Jahrgang 1981, Eintritt mit 30, heute 45, Altersrente 6.000 € pro Jahr ab 67.

| Bilanz | Verfahren | Zins | Rückstellung |
|---|---|---|---|
| Steuerbilanz | Teilwert | 6,00 % | 10.943 € |
| Handelsbilanz | PUC | 2,25 % | 20.140 € |
| (Vergleich) | Teilwert | 2,25 % | 25.685 € |

HGB-Wert / Steuerwert = 1,84

## 3. Zinssensitivität

Duration der Verpflichtung (Alter 45): **31,7 Jahre**. Näherung: 1 Prozentpunkt weniger Zins erhöht die Rückstellung um etwa 31 %.

| Zins | PUC | Änderung |
|---|---|---|
| 1,25 % | 27.578 € | +36,9 % |
| 1,75 % | 23.542 € | +16,9 % |
| 2,25 % | 20.140 € | +0,0 % |
| 2,75 % | 17.264 € | -14,3 % |
| 3,25 % | 14.829 € | -26,4 % |

## 4. Bewertung eines Bestands

Fiktiver Bestand mit 10 Aktiven und 4 Rentnern (`data/bestand.csv`). Jede Person wird mit der Kohortentafel ihres Geburtsjahrgangs und Geschlechts bewertet.

| Person | Status | m/w | Jahrgang | Alter | Rente p.a. | Steuerbilanz (Teilwert, 6 %) | Handelsbilanz (PUC) |
|---|---|---|---|---|---|---|---|
| A01 | aktiv | w | 1998 | 28 | 3.600 € | 762 € | 1.792 € |
| A02 | aktiv | m | 1993 | 33 | 4.200 € | 1.932 € | 4.115 € |
| A03 | aktiv | w | 1989 | 37 | 6.000 € | 4.583 € | 9.518 € |
| A04 | aktiv | m | 1985 | 41 | 4.800 € | 5.983 € | 11.585 € |
| A05 | aktiv | m | 1981 | 45 | 6.000 € | 10.943 € | 20.140 € |
| A06 | aktiv | w | 1977 | 49 | 7.200 € | 19.030 € | 33.837 € |
| A07 | aktiv | m | 1974 | 52 | 9.000 € | 31.167 € | 53.080 € |
| A08 | aktiv | w | 1970 | 56 | 5.400 € | 24.851 € | 39.947 € |
| A09 | aktiv | m | 1966 | 60 | 8.400 € | 51.825 € | 77.863 € |
| A10 | aktiv | m | 1962 | 64 | 10.800 € | 90.965 € | 129.030 € |
| R01 | rentner | m | 1958 | 68 | 7.800 € | 80.928 € | 108.320 € |
| R02 | rentner | m | 1954 | 72 | 9.600 € | 88.885 € | 114.240 € |
| R03 | rentner | w | 1949 | 77 | 6.600 € | 57.556 € | 72.106 € |
| R04 | rentner | m | 1943 | 83 | 5.400 € | 31.224 € | 35.972 € |
| **Summe** | | | | | | **500.634 €** | **711.545 €** |

Differenz Handelsbilanz minus Steuerbilanz: **210.911 €**.

Zins −0,5 Prozentpunkte → 764.360 € (+7,4 %), Zins +0,5 Prozentpunkte → 664.571 € (-6,6 %).

Effektive Duration des Bestands: **14,0 Jahre** (§ 253 Abs. 2 HGB erlaubt pauschal eine Restlaufzeit von 15 Jahren).

## 5. Langlebigkeitsrisiko

Handelsbilanz (PUC) unter den drei Destatis-Annahmen zum Anstieg der Lebenserwartung:

| Variante | Mann 1981 | Frau 1981 | Bestand | Änderung Bestand |
|---|---|---|---|---|
| 1 (niedrig) | 18.835 € | 22.852 € | 691.155 € | -2,9 % |
| 2 (mittel) | 20.140 € | 24.047 € | 711.545 € | +0,0 % |
| 3 (hoch) | 21.625 € | 25.375 € | 733.814 € | +3,1 % |

Zum Vergleich mit der Gompertz-Modelltafel: 761.409 € (+7,0 %).

## 6. Zinsentwicklung und Rückstellung 2015 bis 2026

Derselbe Bestand (Stand heute), bewertet mit dem HGB-Zins verschiedener Stichtage:

| Stichtag | HGB-Zins (15 J.) | Rückstellung (PUC) |
|---|---|---|
| 2015-12-31 | 4,31 % | 547.386 € |
| 2016-12-31 | 4,01 % | 567.008 € |
| 2017-12-31 | 3,68 % | 590.055 € |
| 2018-12-31 | 3,21 % | 625.814 € |
| 2019-12-31 | 2,71 % | 668.134 € |
| 2020-12-31 | 2,30 % | 706.600 € |
| 2021-12-31 | 1,87 % | 751.103 € |
| 2022-12-31 | 1,78 % | 761.009 € |
| 2023-12-31 | 1,82 % | 756.580 € |
| 2024-12-31 | 1,90 % | 747.848 € |
| 2025-12-31 | 2,06 % | 730.878 € |
| 2026-09-30 | 2,25 % | 711.545 € |
