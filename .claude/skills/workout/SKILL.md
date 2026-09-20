---
name: workout
description: Erstellt Lauf-Workouts für Garmin Connect aus einer kompakten Vorlage (workouts/<person>/*.json) mit HF- oder Pace-Bereichen aus dem Trainingsprofil der Person, prüft die Struktur, lädt sie nach Bestätigung hoch und plant sie im Garmin-Kalender ein. Deutsch, Pace min/km.
argument-hint: "[Beschreibung des Trainings | pfad/zur/vorlage.json] [--upload] [--schedule YYYY-MM-DD]"
---

# Workout für Garmin Connect

Du erstellst strukturierte Lauf-Workouts und bringst sie auf Wunsch nach Garmin Connect. Werkzeug ist
`scripts/garmin_workout.py` (Format der Vorlage im Docstring); die Anmeldung läuft wie beim MCP-Server über
`scripts/garmin_auth.py`.

## Regeln

- Die Person kommt aus `mcp__garmin__login_status` (`logged_in_as`): einmal pro Session aufrufen, das Konto
  nennen. Vorlagen liegen unter `workouts/<person>/` (`marc` oder `saskia`), nie im Ordner der anderen Person.
- Zonen und Schwellenwerte aus `workouts/<person>/profil.md` verwenden (Coach-Zonen), nicht die Garmin-Zonen der
  Uhr. Fehlt das Profil oder eine Zone, nachfragen, nichts schätzen.
- Sportart nach Inhalt: Läufe `"sport": "running"`, Rad `"cycling"`, **Hyrox, Stationen, Rudern, Ski Erg und gemischte
  Einheiten immer `"cardio"`**, Kraft `"strength"`. Grund: Ein Uhrenprofil zeigt unter Training → Meine Workouts nur
  Workouts seiner eigenen Sportart; `"other"` erscheint in keinem Profil, nur als Kalender-Workout des Tages, und ein
  „An Gerät senden“ gibt es in der API nicht. Saskia startet Cardio-Workouts auf der fenix 5 im Profil „Hybrid“
  (Kopie von Cardio, siehe `workouts/saskia/profil.md`).
- Vor dem Einplanen `uv run scripts/garmin_workout.py scheduled <YYYY-MM>` aufrufen und prüfen, dass an dem Tag kein
  Doppeleintrag entsteht.
- Vorlagen enthalten nur Trainingsinhalte, keine Zugangsdaten.
- **Hochladen, Einplanen und Löschen nur nach ausdrücklicher Bestätigung** der Person im Chat. Vorher immer die
  Struktur zeigen (`show`).

## Ablauf

1. Training verstehen: Schritte, Dauer oder Distanz je Schritt, Zielbereich (HF-Zone oder Pace-Zone aus dem
   Profil). Bei Coach-Vorgaben (Screenshot, Text) die Vorgabe eins zu eins übernehmen.
2. Vorlage als JSON unter `workouts/<person>/<kurzname>.json` anlegen (Format: `name`, `sport`, `description`, `steps`
   mit `type`, `minutes`/`km`, `hr` [von, bis] oder `pace` ["langsam", "schnell"], `repeat` mit `steps`, optional `note`).
3. Prüfen und zeigen: `uv run scripts/garmin_workout.py show <vorlage>` – Struktur im Chat wiedergeben.
4. Nach Bestätigung: `uv run scripts/garmin_workout.py upload <vorlage>` (liefert `workout_id`), optional
   `uv run scripts/garmin_workout.py schedule <workout_id> <YYYY-MM-DD>`.
5. Vorlage committen (ohne IDs oder Tokens), Ergebnis kurz zusammenfassen.

Weitere Befehle: `list` (Workouts im Konto), `scheduled <YYYY-MM>` (Kalender), `unschedule <scheduled_workout_id>` und
`delete <workout_id>` (beides nur nach Bestätigung).
