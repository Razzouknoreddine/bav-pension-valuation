"""Reproduziert alle Ergebnisse des Projekts.

Schreibt die Grafiken nach docs/figures/ und die Tabellen nach docs/results.md.
Aufruf:  python scripts/run_experiments.py
"""
import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from bavpension import (KohortenSterbetafel, Sterbetafel, bewerte_bestand, duration,
                        hgb_zins, lade_bestand, leibrente, leistungsbarwert, puc,
                        stichtage, teilwert)

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "docs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
INK, MUTED = "#1f1f1e", "#6b6b66"
plt.rcParams.update({
    "figure.dpi": 130, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.grid": True, "grid.color": "#e6e5df",
    "grid.linewidth": 0.6, "lines.linewidth": 2, "legend.frameon": False,
    "axes.titleweight": "bold", "axes.titlesize": 11,
})

# ----------------------------- Annahmen -----------------------------------
STICHTAG = stichtage()[-1]                 # letzter Bundesbank-Wert
ZINS_HGB = hgb_zins(STICHTAG, 15)          # § 253 Abs. 2 HGB, pauschal 15 Jahre
ZINS_STEUER = 0.06                         # § 6a EStG
Z = 67                                     # Pensionierungsalter
VARIANTE = 2                               # Destatis: mittlerer Anstieg der Lebenserwartung

# Beispielmitarbeiter: Mann, Jahrgang 1981, Eintritt mit 30, heute 45, Rente 6.000 € p.a.
JG, G, E, X, R = 1981, "m", 30, 45, 6000
T = KohortenSterbetafel(JG, G, VARIANTE)

md = ["# Ergebnisse", "", "Erzeugt von `scripts/run_experiments.py`.", "",
      f"Stichtag {STICHTAG}, HGB-Zins (15 Jahre) {ZINS_HGB * 100:.2f} %, Steuerzins 6 %, "
      f"Destatis-Kohortentafeln Variante {VARIANTE}.".replace(".", ",", 1), ""]


def eur(v):
    return f"{v:,.0f} €".replace(",", ".")


def pct(v, d=2):
    return f"{v * 100:.{d}f} %".replace(".", ",")


def num(v, d=1, sign=False):
    return (f"{v:+.{d}f}" if sign else f"{v:.{d}f}").replace(".", ",")


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG / name, bbox_inches="tight")
    plt.close(fig)


def kohorte(p, variante=VARIANTE):
    return KohortenSterbetafel(p.geburtsjahr, p.geschlecht, variante)


# ----------------------------- 1. Sterbetafeln -----------------------------
gompertz = Sterbetafel()
md += ["## 1. Sterbetafeln", "",
       "Restlebenserwartung mit 67 und Rentenbarwertfaktor $\\ddot a_{67}$ (HGB-Zins):", "",
       "| Tafel | $e_{67}$ | $\\ddot a_{67}$ |", "|---|---|---|"]
for name, t in [("Gompertz-Makeham (Modell)", gompertz)] + [
        (f"Destatis Jahrgang {JG}, {'Mann' if g == 'm' else 'Frau'}, Variante {v}", KohortenSterbetafel(JG, g, v))
        for g in "mw" for v in (1, 2, 3)]:
    md.append(f"| {name} | {num(t.lebenserwartung(67))} Jahre | {num(leibrente(t, 67, ZINS_HGB), 2)} |")
md.append("")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.9))
alter = list(range(30, 100))
a1.semilogy(alter, [KohortenSterbetafel(JG, "m", VARIANTE).qx(x) for x in alter], color=C[0], label=f"Destatis {JG}, Mann")
a1.semilogy(alter, [KohortenSterbetafel(JG, "w", VARIANTE).qx(x) for x in alter], color=C[4], label=f"Destatis {JG}, Frau")
a1.semilogy(alter, [gompertz.qx(x) for x in alter], "--", color=MUTED, lw=1.5, label="Gompertz-Makeham")
a1.set(title="Sterbewahrscheinlichkeit $q_x$", xlabel="Alter x")
a1.legend()
jahrgaenge = list(range(1930, 2001))
for v, farbe in zip((1, 2, 3), (C[2], C[0], C[1])):
    a2.plot(jahrgaenge, [KohortenSterbetafel(j, "m", v).lebenserwartung(67) for j in jahrgaenge],
            color=farbe, label=f"Variante {v}")
a2.set(title="Lebenserwartung mit 67 nach Jahrgang (Männer)", xlabel="Geburtsjahrgang", ylabel="Jahre")
a2.legend()
save(fig, "sterbetafel.png")

# ----------------------------- 2. Einzelbewertung --------------------------
tw = teilwert(T, E, X, Z, R, ZINS_STEUER)
pu = puc(T, E, X, Z, R, ZINS_HGB)
md += ["## 2. Einzelbewertung", "",
       f"Mann, Jahrgang {JG}, Eintritt mit {E}, heute {X}, Altersrente {eur(R)} pro Jahr ab {Z}.", "",
       "| Bilanz | Verfahren | Zins | Rückstellung |", "|---|---|---|---|",
       f"| Steuerbilanz | Teilwert | {pct(ZINS_STEUER)} | {eur(tw)} |",
       f"| Handelsbilanz | PUC | {pct(ZINS_HGB)} | {eur(pu)} |",
       f"| (Vergleich) | Teilwert | {pct(ZINS_HGB)} | {eur(teilwert(T, E, X, Z, R, ZINS_HGB))} |",
       "", f"HGB-Wert / Steuerwert = {num(pu / tw, 2)}", ""]

xs = list(range(E, Z + 1))
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(xs, [leistungsbarwert(T, x, Z, R, ZINS_HGB) for x in xs], "--", color=MUTED, lw=1.5, label="Leistungsbarwert (HGB-Zins)")
ax.plot(xs, [puc(T, E, x, Z, R, ZINS_HGB) for x in xs], color=C[0], label=f"PUC, Handelsbilanz ({pct(ZINS_HGB)})")
ax.plot(xs, [teilwert(T, E, x, Z, R, ZINS_HGB) for x in xs], color=C[2], label=f"Teilwert ({pct(ZINS_HGB)})")
ax.plot(xs, [teilwert(T, E, x, Z, R, ZINS_STEUER) for x in xs], color=C[1], label=f"Teilwert, Steuerbilanz ({pct(ZINS_STEUER, 0)})")
ax.set(title=f"Aufbau der Pensionsrückstellung (Mann, Jahrgang {JG})", xlabel="Alter des Mitarbeiters", ylabel="Rückstellung in €")
ax.legend()
save(fig, "rueckstellung.png")

# ----------------------------- 3. Zinssensitivität -------------------------
D = duration(T, X, Z, ZINS_HGB)
md += ["## 3. Zinssensitivität", "",
       f"Duration der Verpflichtung (Alter {X}): **{num(D)} Jahre**. "
       f"Näherung: 1 Prozentpunkt weniger Zins erhöht die Rückstellung um etwa {D / (1 + ZINS_HGB):.0f} %.", "",
       "| Zins | PUC | Änderung |", "|---|---|---|"]
for d in (-0.01, -0.005, 0, 0.005, 0.01):
    v = puc(T, E, X, Z, R, ZINS_HGB + d)
    md.append(f"| {pct(ZINS_HGB + d)} | {eur(v)} | {num((v / pu - 1) * 100, sign=True)} % |")
md.append("")

zinsen = [i / 1000 for i in range(5, 71)]
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot([i * 100 for i in zinsen], [puc(T, E, X, Z, R, i) for i in zinsen], color=C[0], label="PUC")
ax.plot([i * 100 for i in zinsen], [teilwert(T, E, X, Z, R, i) for i in zinsen], color=C[1], label="Teilwert")
for i, txt in [(ZINS_HGB, "HGB"), (ZINS_STEUER, "§ 6a EStG")]:
    ax.axvline(i * 100, color=MUTED, lw=1, ls=":")
    ax.text(i * 100 + 0.1, ax.get_ylim()[1] * 0.92, txt, color=MUTED)
ax.set(title=f"Rückstellung in Abhängigkeit vom Rechnungszins (Alter {X})", xlabel="Rechnungszins in %", ylabel="Rückstellung in €")
ax.legend()
save(fig, "zinssensitivitaet.png")

# ----------------------------- 4. Bestandsbewertung ------------------------
bestand = lade_bestand(ROOT / "data" / "bestand.csv")
s_hgb, e_hgb = bewerte_bestand(kohorte, bestand, "PUC", ZINS_HGB, Z)
s_st, e_st = bewerte_bestand(kohorte, bestand, "Teilwert", ZINS_STEUER, Z)
s_up, _ = bewerte_bestand(kohorte, bestand, "PUC", ZINS_HGB + 0.005, Z)
s_dn, _ = bewerte_bestand(kohorte, bestand, "PUC", ZINS_HGB - 0.005, Z)
n_akt = sum(p.status == "aktiv" for p in bestand)
d_bestand = (s_dn - s_up) / (2 * s_hgb * 0.005)

md += ["## 4. Bewertung eines Bestands", "",
       f"Fiktiver Bestand mit {n_akt} Aktiven und {len(bestand) - n_akt} Rentnern (`data/bestand.csv`). "
       "Jede Person wird mit der Kohortentafel ihres Geburtsjahrgangs und Geschlechts bewertet.", "",
       "| Person | Status | m/w | Jahrgang | Alter | Rente p.a. | Steuerbilanz (Teilwert, 6 %) | Handelsbilanz (PUC) |",
       "|---|---|---|---|---|---|---|---|"]
for p in bestand:
    md.append(f"| {p.id} | {p.status} | {p.geschlecht} | {p.geburtsjahr} | {p.alter} | {eur(p.rente)} | {eur(e_st[p.id])} | {eur(e_hgb[p.id])} |")
md += [f"| **Summe** | | | | | | **{eur(s_st)}** | **{eur(s_hgb)}** |", "",
       f"Differenz Handelsbilanz minus Steuerbilanz: **{eur(s_hgb - s_st)}**.", "",
       f"Zins −0,5 Prozentpunkte → {eur(s_dn)} ({num((s_dn / s_hgb - 1) * 100, sign=True)} %), "
       f"Zins +0,5 Prozentpunkte → {eur(s_up)} ({num((s_up / s_hgb - 1) * 100, sign=True)} %).", "",
       f"Effektive Duration des Bestands: **{num(d_bestand)} Jahre** "
       "(§ 253 Abs. 2 HGB erlaubt pauschal eine Restlaufzeit von 15 Jahren).", ""]

fig, ax = plt.subplots(figsize=(9, 4.2))
ids = [p.id for p in bestand]
pos = range(len(ids))
ax.bar([i - 0.2 for i in pos], [e_st[k] for k in ids], 0.4, color=C[1], label="Steuerbilanz (Teilwert, 6 %)")
ax.bar([i + 0.2 for i in pos], [e_hgb[k] for k in ids], 0.4, color=C[0], label=f"Handelsbilanz (PUC, {pct(ZINS_HGB)})")
ax.set_xticks(list(pos), ids)
ax.set(title="Pensionsrückstellung je Person", ylabel="Rückstellung in €")
ax.legend()
save(fig, "bestand.png")

# ----------------------------- 5. Langlebigkeitsrisiko ---------------------
md += ["## 5. Langlebigkeitsrisiko", "",
       "Handelsbilanz (PUC) unter den drei Destatis-Annahmen zum Anstieg der Lebenserwartung:", "",
       f"| Variante | Mann {JG} | Frau {JG} | Bestand | Änderung Bestand |", "|---|---|---|---|---|"]
basis = s_hgb
werte_v = {}
for v in (1, 2, 3):
    sb, _ = bewerte_bestand(lambda p: kohorte(p, v), bestand, "PUC", ZINS_HGB, Z)
    werte_v[v] = sb
    md.append(f"| {v} ({['niedrig', 'mittel', 'hoch'][v - 1]}) | {eur(puc(KohortenSterbetafel(JG, 'm', v), E, X, Z, R, ZINS_HGB))} "
              f"| {eur(puc(KohortenSterbetafel(JG, 'w', v), E, X, Z, R, ZINS_HGB))} | {eur(sb)} | {num((sb / basis - 1) * 100, sign=True)} % |")
s_gomp, _ = bewerte_bestand(gompertz, bestand, "PUC", ZINS_HGB, Z)
md += ["", f"Zum Vergleich mit der Gompertz-Modelltafel: {eur(s_gomp)} ({num((s_gomp / basis - 1) * 100, sign=True)} %).", ""]

# ----------------------------- 6. Zinsentwicklung 2015-2026 ----------------
tage = [t for t in stichtage() if t.endswith("12-31")] + [STICHTAG]
md += ["## 6. Zinsentwicklung und Rückstellung 2015 bis 2026", "",
       "Derselbe Bestand (Stand heute), bewertet mit dem HGB-Zins verschiedener Stichtage:", "",
       "| Stichtag | HGB-Zins (15 J.) | Rückstellung (PUC) |", "|---|---|---|"]
verlauf = []
for t in tage:
    i = hgb_zins(t, 15)
    s, _ = bewerte_bestand(kohorte, bestand, "PUC", i, Z)
    verlauf.append((t, i, s))
    md.append(f"| {t} | {pct(i)} | {eur(s)} |")
md.append("")

alle = stichtage()
datum = lambda t: datetime.date.fromisoformat(t)
fig, a1 = plt.subplots(figsize=(9, 4.4))
a1.plot([datum(t) for t in alle], [hgb_zins(t, 15) * 100 for t in alle], color=C[0], label="HGB-Zins 15 Jahre (linke Achse)")
a1.set_ylabel("Zins in %")
a2 = a1.twinx()
a2.plot([datum(t) for t, _, _ in verlauf], [s / 1000 for _, _, s in verlauf], "o-", color=C[1],
        label="Rückstellung des Bestands, PUC (rechte Achse)")
a2.set_ylabel("Rückstellung in Tsd. €")
a2.spines["right"].set_visible(True)
a2.grid(False)
h1, l1 = a1.get_legend_handles_labels()
h2, l2 = a2.get_legend_handles_labels()
a1.legend(h1 + h2, l1 + l2, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)
a1.set_title("Bundesbank-Rechnungszins und Pensionsrückstellung 2015 bis 2026")
save(fig, "zinsentwicklung.png")

(ROOT / "docs" / "results.md").write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
