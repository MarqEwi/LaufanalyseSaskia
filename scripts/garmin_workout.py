# /// script
# requires-python = ">=3.11"
# dependencies = ["garminconnect>=0.3.2", "pydantic>=2"]
# ///
"""Lauf-Workouts für Garmin Connect aus einer kompakten Vorlage bauen, prüfen, hochladen und einplanen.

Vorlagen liegen unter workouts/<person>/<name>.json (Person = logged_in_as aus login_status). Format:

    {
      "name": "Schwelle 3x10min",
      "description": "optional",
      "steps": [
        {"type": "warmup",   "minutes": 10, "hr": [90, 134]},
        {"repeat": 3, "steps": [
            {"type": "interval", "minutes": 10, "hr": [150, 156]},
            {"type": "recovery", "minutes": 3,  "hr": [90, 134]}
        ]},
        {"type": "cooldown", "km": 1.0, "pace": ["6:55", "6:07"]}
      ]
    }

  sport:   "running" (Standard) oder "other" (gemischte Einheiten mit Stationen, z. B. Hyrox)
  type:    warmup | interval | recovery | rest | cooldown
  Dauer:   "minutes" (Zeit), "km" (Distanz) oder "lap": true (Ende per Lap-Taste, für Stationen ohne Messung), genau eins
  note:    Text, den die Uhr zum Schritt anzeigt (Stationsname, RPE)
  Ziel:    "hr": [von, bis] in bpm  oder  "pace": ["langsam", "schnell"] in m:ss min/km  oder nichts (kein Ziel)
  repeat:  Wiederholungsgruppe mit "steps"

Befehle (alle ohne Nebenwirkung außer upload/schedule/delete):

    uv run scripts/garmin_workout.py show   workouts/saskia/schwelle-3x10min.json   # Struktur + Garmin-JSON prüfen
    uv run scripts/garmin_workout.py upload workouts/saskia/schwelle-3x10min.json   # nach Garmin Connect hochladen
    uv run scripts/garmin_workout.py schedule <workout_id> 2026-09-24               # im Garmin-Kalender einplanen
    uv run scripts/garmin_workout.py list                                           # Workouts im Konto
    uv run scripts/garmin_workout.py delete <workout_id>

Hochladen, Einplanen und Löschen nur nach ausdrücklicher Bestätigung der Person (CLAUDE.md).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

STEP_TYPES = {
    "warmup": (1, "warmup", 1),
    "cooldown": (2, "cooldown", 2),
    "interval": (3, "interval", 3),
    "recovery": (4, "recovery", 4),
    "rest": (5, "rest", 5),
}


def _pace_to_mps(pace: str) -> float:
    m, s = pace.strip().split(":")
    sec_per_km = int(m) * 60 + int(s)
    return 1000.0 / sec_per_km


def _mps_to_pace(mps: float) -> str:
    sec = round(1000.0 / mps)
    return f"{sec // 60}:{sec % 60:02d}"


def _target(step: dict[str, Any]) -> dict[str, Any]:
    if "hr" in step:
        lo, hi = step["hr"]
        if not (0 < lo < hi < 250):
            raise ValueError(f"HF-Bereich unplausibel: {step['hr']}")
        return {
            "targetType": {"workoutTargetTypeId": 4, "workoutTargetTypeKey": "heart.rate.zone", "displayOrder": 4},
            "targetValueOne": float(lo),
            "targetValueTwo": float(hi),
            "zoneNumber": None,
        }
    if "pace" in step:
        slow, fast = step["pace"]
        v_slow, v_fast = _pace_to_mps(slow), _pace_to_mps(fast)
        if v_slow >= v_fast:
            raise ValueError(f"Pace-Bereich: erst langsam, dann schnell angeben: {step['pace']}")
        return {
            "targetType": {"workoutTargetTypeId": 5, "workoutTargetTypeKey": "speed.zone", "displayOrder": 5},
            "targetValueOne": v_slow,
            "targetValueTwo": v_fast,
            "zoneNumber": None,
        }
    return {"targetType": {"workoutTargetTypeId": 1, "workoutTargetTypeKey": "no.target", "displayOrder": 1}}


def _end(step: dict[str, Any]) -> tuple[dict[str, Any], float, float]:
    """Endbedingung, Wert, geschätzte Dauer in Sekunden."""
    given = [k for k in ("minutes", "km", "lap") if k in step]
    if len(given) != 1:
        raise ValueError(f"Schritt braucht genau eins von 'minutes', 'km' oder 'lap': {step}")
    if "lap" in step:
        return ({"conditionTypeId": 1, "conditionTypeKey": "lap.button", "displayOrder": 1, "displayable": True}, 0.0,
                float(step.get("estimate_minutes", 2)) * 60)
    if "minutes" in step:
        secs = float(step["minutes"]) * 60
        return ({"conditionTypeId": 2, "conditionTypeKey": "time", "displayOrder": 2, "displayable": True}, secs, secs)
    meters = float(step["km"]) * 1000
    # Dauer-Schätzung nur für estimatedDurationInSecs (Anzeige), 6:00 min/km falls keine Pace vorgegeben
    mps = _pace_to_mps(step["pace"][0]) if "pace" in step else 1000 / 360
    return ({"conditionTypeId": 3, "conditionTypeKey": "distance", "displayOrder": 3, "displayable": True}, meters, meters / mps)


def _build_steps(steps: list[dict[str, Any]], order: list[int]) -> tuple[list[dict[str, Any]], float]:
    out: list[dict[str, Any]] = []
    total = 0.0
    for step in steps:
        order[0] += 1
        if "repeat" in step:
            n = int(step["repeat"])
            group_order = order[0]
            children, child_secs = _build_steps(step["steps"], order)
            out.append({
                "type": "RepeatGroupDTO",
                "stepOrder": group_order,
                "stepType": {"stepTypeId": 6, "stepTypeKey": "repeat", "displayOrder": 6},
                "numberOfIterations": n,
                "smartRepeat": False,
                "endCondition": {"conditionTypeId": 7, "conditionTypeKey": "iterations", "displayOrder": 7, "displayable": False},
                "endConditionValue": float(n),
                "workoutSteps": children,
            })
            total += n * child_secs
            continue
        t = step.get("type")
        if t not in STEP_TYPES:
            raise ValueError(f"Unbekannter Schritttyp {t!r} (erlaubt: {', '.join(STEP_TYPES)})")
        type_id, key, disp = STEP_TYPES[t]
        end, value, secs = _end(step)
        d: dict[str, Any] = {
            "type": "ExecutableStepDTO",
            "stepOrder": order[0],
            "stepType": {"stepTypeId": type_id, "stepTypeKey": key, "displayOrder": disp},
            "endCondition": end,
            "endConditionValue": value,
        }
        d.update(_target(step))
        if step.get("note"):
            d["description"] = str(step["note"])
        out.append(d)
        total += secs
    return out, total


def build(spec: dict[str, Any]) -> dict[str, Any]:
    steps, secs = _build_steps(spec["steps"], [0])
    sports = {"running": {"sportTypeId": 1, "sportTypeKey": "running", "displayOrder": 1},
              "other": {"sportTypeId": 3, "sportTypeKey": "other", "displayOrder": 13}}
    sport_key = spec.get("sport", "running")
    if sport_key not in sports:
        raise ValueError(f"sport muss running oder other sein, nicht {sport_key!r}")
    sport = sports[sport_key]
    payload = {
        "workoutName": spec["name"],
        "description": spec.get("description"),
        "sportType": sport,
        "estimatedDurationInSecs": int(round(secs)),
        "workoutSegments": [{"segmentOrder": 1, "sportType": sport, "workoutSteps": steps}],
    }
    from garminconnect.workout import BaseWorkout  # Struktur gegen die Bibliotheksmodelle prüfen

    return BaseWorkout(**payload).to_dict()


def _describe(steps: list[dict[str, Any]], indent: str = "") -> list[str]:
    lines = []
    for s in steps:
        if s["type"] == "RepeatGroupDTO":
            lines.append(f"{indent}{s['numberOfIterations']} ×")
            lines += _describe(s["workoutSteps"], indent + "    ")
            continue
        kind = s["stepType"]["stepTypeKey"]
        if s["endCondition"]["conditionTypeKey"] == "time":
            v = s["endConditionValue"]
            dur = f"{int(v // 60)}:{int(v % 60):02d} min"
        elif s["endCondition"]["conditionTypeKey"] == "lap.button":
            dur = "Lap-Taste"
        else:
            dur = f"{s['endConditionValue'] / 1000:.2f} km"
        tt = s["targetType"]["workoutTargetTypeKey"]
        if tt == "heart.rate.zone":
            target = f"HF {int(s['targetValueOne'])}–{int(s['targetValueTwo'])} bpm"
        elif tt == "speed.zone":
            target = f"Pace {_mps_to_pace(s['targetValueOne'])}–{_mps_to_pace(s['targetValueTwo'])} min/km"
        else:
            target = "kein Ziel"
        note = f"  ({s['description']})" if s.get("description") else ""
        lines.append(f"{indent}{kind:9s} {dur:>10s}  {target}{note}")
    return lines


def _load_spec(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _client():
    import garmin_auth

    client = garmin_auth.connect(interactive=False)
    print(f"Angemeldet als: {garmin_auth.whoami(client)}", file=sys.stderr)
    return client


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("show", help="Vorlage prüfen und Struktur anzeigen (ohne Garmin-Zugriff)")
    p.add_argument("spec", type=Path)
    p.add_argument("--json", action="store_true", help="fertiges Garmin-JSON ausgeben")
    p = sub.add_parser("upload", help="Vorlage nach Garmin Connect hochladen")
    p.add_argument("spec", type=Path)
    p = sub.add_parser("schedule", help="Workout im Garmin-Kalender einplanen")
    p.add_argument("workout_id", type=int)
    p.add_argument("date", help="YYYY-MM-DD")
    sub.add_parser("list", help="Workouts im Konto auflisten")
    p = sub.add_parser("delete", help="Workout aus dem Konto löschen")
    p.add_argument("workout_id", type=int)
    args = ap.parse_args()

    if args.cmd == "show":
        payload = build(_load_spec(args.spec))
        print(f"{payload['workoutName']}  [{payload['sportType']['sportTypeKey']}]  (geschätzt {payload['estimatedDurationInSecs'] // 60} min)")
        if payload.get("description"):
            print(payload["description"])
        print("\n".join(_describe(payload["workoutSegments"][0]["workoutSteps"])))
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "upload":
        payload = build(_load_spec(args.spec))
        res = _client().upload_workout(payload)
        print(f"Hochgeladen: '{res.get('workoutName')}' → workout_id {res.get('workoutId')}")
        return 0

    if args.cmd == "schedule":
        res = _client().schedule_workout(args.workout_id, args.date)
        print(f"Eingeplant für {args.date}: scheduled_workout_id {res.get('workoutScheduleId', res)}")
        return 0

    if args.cmd == "list":
        for w in _client().get_workouts(0, 50):
            print(f"{w.get('workoutId')}  {w.get('workoutName')}  ({w.get('sportType', {}).get('sportTypeKey')}, "
                  f"geändert {str(w.get('updateDate') or w.get('updatedDate') or '')[:10]})")
        return 0

    if args.cmd == "delete":
        _client().delete_workout(args.workout_id)
        print(f"Gelöscht: workout_id {args.workout_id}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
