# Laufanalyse – Hinweise für Claude Code

## Ordner-Konvention auf dem PC (Windows)

- Neue Projektordner auf dem PC des Nutzers immer unter `E:\Users\Marc\Claude Projekte\<Projektname>` anlegen, nie an anderer Stelle.
- Dieses Repo liegt auf dem PC unter `E:\Users\Marc\Claude Projekte\GarminConnect`.
- Exportierte Laufdaten gehören nach `E:\Users\Marc\Claude Projekte\GarminConnect\data\garmin\<datum>_<id>\` (das ist `LAUFANALYSE_DATA_DIR`, wird vom Setup-Skript gesetzt).
- Token-Cache bleibt bewusst außerhalb des Projekts in `%USERPROFILE%\.garminconnect` (nicht versioniert).

## Profile (zwei Personen, ein Repo)

| Cloud-Umgebung | Garmin-Konto | Workout-Vorlagen |
|---|---|---|
| „Laufanalyse Marc“ | Marq Ewi | `workouts/marc/` |
| „Laufanalyse Saskia“ | Saskia | `workouts/saskia/` |

- Die Person ergibt sich **nur** aus `mcp__garmin__login_status` (`logged_in_as`), nie aus dem Repo, dem Branch oder der Ordnerstruktur.
- Zu Beginn jeder Session, die auf Garmin zugreift, einmal `mcp__garmin__login_status` aufrufen und nennen, wessen Konto verbunden ist. Passt der Name nicht zur Umgebung: stoppen und nachfragen.
- Zugangsdaten und Tokens liegen pro Umgebung (`GARMIN_EMAIL`, `GARMIN_PASSWORD` nur bis zum ersten Token, danach `GARMIN_TOKENS_B64`). Das Konto der jeweils anderen Person wird nie angefasst.
- Datenordner sind pro Umgebung getrennt: `LAUFANALYSE_DATA_DIR` setzt der Session-Start-Hook (`.claude/hooks/session-start.sh`) bzw. die Umgebung.
- Workout-Vorlagen liegen unter `workouts/<person>/` (`marc` oder `saskia`, Kleinbuchstaben); die Skill `/workout` speichert nach der Person aus `login_status`.
- Trainingsprofil je Person unter `workouts/<person>/profil.md` (Coach-Zonen, Schwellenwerte). Saskia: Coach Nils, LTHR 158 bpm (Eingangstest 10.06.2026), Pace-Zonen „Laufzonen NEU“ vom 20.09.2026 (Schwelle 4:43–5:04 min/km), Details in `workouts/saskia/profil.md`. Für Trainingsplanung und Workout-Vorlagen gelten die Coach-Zonen aus dem Profil, nicht die Garmin-Zonen. Saskias Uhr: Garmin fenix 5 (keine Laufdynamik/Leistung ohne Zubehör), Uhrenprofil „Hybrid“ (Kopie von Cardio) für Cardio-Workouts. Sportart der Workouts: Läufe `running`, Hyrox/Stationen/gemischt `cardio`, nie `other` (siehe Skill `/workout`). Wettkampfziel: Hyrox Hamburg Women Pro am 30.10.2026, Trainingsziel Hyrox Pro.
- Zweite Person am Windows-PC: eigener Token-Ordner `%USERPROFILE%\.garminconnect-saskia`, siehe `docs/garmin-tools.md` Abschnitt 2a.

## Regeln für dieses Projekt

- Deutsch in allen Ausgaben, Pace in min/km, Distanzen in km, Zeiten als mm:ss.
- Keine Zugangsdaten oder Tokens in Dateien des Repos; `.gitignore` beachten.
- Liefert ein Tool nicht die erwarteten Daten: klar sagen und Alternative vorschlagen, nie Werte schätzen.
- Laufanalysen laufen über die Skill `/laufanalyse` und den MCP-Server `garmin` (`scripts/garmin_mcp_server.py`, registriert in `.mcp.json`).
- Tool-Referenz: `docs/garmin-tools.md`.
