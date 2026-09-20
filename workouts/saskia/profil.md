# Trainingsprofil Saskia

Grundlage für Trainingsplanung, Workout-Vorlagen und die Einordnung von Läufen. Quellen: Eingangstest durch
Coach Nils (Coach-App, 10.06.2026) für HF-Zonen und LTHR; „Laufzonen NEU“ aus der Coach-App (Block B, 20.09.2026,
abgeleitet aus dem 10-km-Lauf vom 18.09.2026) für die Pace-Zonen. Bei neuen Vorgaben diese Datei aktualisieren
und das Datum anpassen.

## Schwellenwerte

| Kennzahl | Wert | Stand |
|---|---|---|
| Laktatschwellen-Herzfrequenz (LTHR) | 158 bpm | Eingangstest 10.06.2026 |
| Schwellenpace (Zone 4) | 4:43 – 5:04 min/km | Laufzonen NEU 20.09.2026 |

## Herzfrequenz-Zonen (Coach Nils, Eingangstest 10.06.2026, weiterhin gültig)

| Zone | Bezeichnung | Herzfrequenz |
|---|---|---|
| 1 | Regeneration | < 134 bpm |
| 2 | Grundlagenausdauer | 134 – 141 bpm |
| 3 | Tempo | 142 – 149 bpm |
| 4 | Schwelle | 150 – 156 bpm |
| 5 | VO2max / Anaerob | > 156 bpm |

## Pace-Zonen („Laufzonen NEU“, Coach-App 20.09.2026, gültig)

| Zone | Bezeichnung | Pace | Geschwindigkeit |
|---|---|---|---|
| 1 | extensive Grundlage / Regeneration | langsamer als 6:05 min/km | unter 9,9 km/h |
| 2 | intensive Grundlage | 5:35 – 6:05 min/km | 9,9 – 10,7 km/h |
| 3 | zügig / Tempo | 5:05 – 5:34 min/km | 10,8 – 11,8 km/h |
| 4 | Schwelle | 4:43 – 5:04 min/km | 11,9 – 12,7 km/h |
| 5 | VO2max | 4:15 – 4:42 min/km | 12,8 – 14,1 km/h |

Für Pace-Ziele in Workout-Vorlagen (`"pace": ["langsam", "schnell"]`) diese Grenzen verwenden.

### Frühere Pace-Zonen (Eingangstest 10.06.2026, ersetzt am 20.09.2026)

| Zone | Pace |
|---|---|
| 1 | langsamer als 6:55 |
| 2 | 6:07 – 6:55 |
| 3 | 5:41 – 6:04 |
| 4 | 5:18 – 5:38 |
| 5 | schneller als 5:18 |

## Hinweise für Planung und Auswertung

- Für Trainingspläne und Workout-Vorlagen gelten diese Coach-Zonen, nicht die Zonen der Garmin-Uhr.
  Die Uhr rechnet mit eigenen Grenzen (Stand 18.09.2026: Zone 4 ab 144 bpm, Zone 5 ab 164 bpm); in
  Laufberichten beide nennen und die Coach-Zonen als Maßstab verwenden.
- Erholungsschwelle für `analyze_run` (`recovery_hr`): Standard 140 bpm passt zur Obergrenze von Zone 2
  (141 bpm); ohne andere Vorgabe so lassen.
- Der 10-km-Lauf vom 18.09.2026 (4:44 min/km bei Ø-HF 158 bpm) war die Grundlage der neuen Pace-Zonen; die
  Pace liegt jetzt in Zone 4. Die HF-Zonen stammen weiterhin aus dem Juni; ob sie noch passen, kann nur ein
  neuer Test klären. Keine eigenen Zonen ableiten, Änderungen kommen vom Coach.
- Uhr: Garmin fenix 5. Sie unterstützt Workouts mit eigenen HF- und Pace-Bereichen (so sind die Vorlagen hier
  gebaut). Laufdynamik (Bodenkontakt, vertikale Bewegung) und Leistung liefert sie nur mit HRM-Run/HRM-Tri-Gurt
  oder Running-Dynamics-Pod; ohne Zubehör fehlen diese Felder in der Analyse, das ist kein Fehler.
- Uhrenprofil „Hybrid“: Kopie des Profils Cardio auf der fenix 5, GPS aus, Auto Lap aus, Auto Pause aus, Rundentaste an.
  Darin erscheinen Workouts der Sportart `cardio` unter Meine Workouts; Hyrox-Einheiten werden dort gestartet.
- Brustgurt: nicht bekannt (nachtragen). Ohne Gurt misst die fenix 5 die HF am Handgelenk; bei Stationen mit
  Griffbelastung (Sled, Carry, Rudern) ist die Handgelenksmessung unzuverlässig.
- Wettkampfziel: Hyrox Hamburg, Women Pro, 30.10.2026. Trainingsziel: Hyrox Pro (Laufabschnitte 8 × 1 km
  zwischen den Stationen, dazu die Kraft-/Ausdauerstationen). Laufeinheiten darauf ausrichten: Schwellen- und
  Tempoarbeit über 1-km-Abschnitte mit kurzen Pausen, Laufen unter Vorermüdung, Grundlage in Zone 2.
