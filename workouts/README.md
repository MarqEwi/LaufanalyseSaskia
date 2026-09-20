# Workout-Vorlagen

Ein Unterordner je Person, Name in Kleinbuchstaben wie in `CLAUDE.md` („Profile“):

| Ordner | Person | Garmin-Konto |
|---|---|---|
| `marc/` | Marc | Marq Ewi |
| `saskia/` | Saskia | Saskia |

Regeln:

- Die Person kommt aus `mcp__garmin__login_status` (`logged_in_as`), nicht aus dem Ordnernamen. Die Skill `/workout`
  speichert und lädt Vorlagen nur im Ordner der angemeldeten Person.
- Vorlagen enthalten nur Trainingsinhalte (Schritte, Dauer/Distanz, Zielbereiche), keine Zugangsdaten, Tokens
  oder Gesundheitsrohdaten.
- Hochladen, Einplanen oder Löschen von Workouts in Garmin Connect nur nach ausdrücklicher Bestätigung der Person.

Format und Werkzeug: Vorlagen sind kompakte JSON-Dateien (`name`, `description`, `steps` mit `type`,
`minutes`/`km`, `hr` oder `pace`, `repeat`), siehe Docstring von `scripts/garmin_workout.py`.
`uv run scripts/garmin_workout.py show <vorlage>` prüft und zeigt die Struktur, `upload` und `schedule`
bringen sie nach Garmin Connect (nur nach Bestätigung). Zonen und Schwellen je Person stehen in
`<person>/profil.md`.
