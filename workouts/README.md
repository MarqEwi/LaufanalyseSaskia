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
