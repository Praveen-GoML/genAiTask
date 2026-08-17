"""
scripts/seed_db.py - populates the fitness tables from the hand-authored, deterministic
rows in src/db/seed_data.py. Safe to re-run: clears the 4 tables (children before
parents, respecting foreign keys) and reinserts from scratch every time, so the DB
always matches whatever's currently in seed_data.py.

Run from the project root (after `python -m scripts.setup_db`):
    python -m scripts.seed_db
"""

from src.db.database import SessionLocal
from src.db.models import ExerciseLog, NutritionLog, WorkoutSession, Member
from src.db.seed_data import MEMBERS, WORKOUT_SESSIONS, EXERCISE_LOGS, NUTRITION_LOGS


def main():
    session = SessionLocal()
    try:
        # Children first — respect foreign key order
        session.query(ExerciseLog).delete()
        session.query(NutritionLog).delete()
        session.query(WorkoutSession).delete()
        session.query(Member).delete()
        session.flush()

        # Insert members
        members_by_name = {}
        for row in MEMBERS:
            member = Member(**row)
            session.add(member)
            members_by_name[row["name"]] = member

        session.flush()  # assigns .id to every member before we reference them

        # Insert workout sessions
        sessions_by_key = {}
        for row in WORKOUT_SESSIONS:
            ws = WorkoutSession(
                member_id=members_by_name[row["member"]].id,
                session_date=row["session_date"],
                session_type=row["session_type"],
                duration_min=row["duration_min"],
                notes=row.get("notes"),
            )
            session.add(ws)
            # Key: (member_name, session_date) — used to resolve exercise log references
            sessions_by_key[(row["member"], row["session_date"])] = ws

        session.flush()  # assigns .id to every WorkoutSession

        # Insert exercise logs
        for row in EXERCISE_LOGS:
            member_name, session_date = row["session"]
            key = (member_name, session_date)
            if key not in sessions_by_key:
                print(f"  WARNING: No session found for {key} — skipping exercise log row.")
                continue
            session.add(ExerciseLog(
                session_id=sessions_by_key[key].id,
                exercise_name=row["exercise_name"],
                sets_completed=row["sets_completed"],
                reps_per_set=row["reps_per_set"],
                weight_kg=row["weight_kg"],
                rpe=row.get("rpe"),
            ))

        # Insert nutrition logs
        for row in NUTRITION_LOGS:
            session.add(NutritionLog(
                member_id=members_by_name[row["member"]].id,
                log_date=row["log_date"],
                calories_kcal=row["calories_kcal"],
                protein_g=row["protein_g"],
                carbs_g=row["carbs_g"],
                fat_g=row["fat_g"],
                water_ml=row.get("water_ml"),
                notes=row.get("notes"),
            ))

        session.commit()
        print(
            f"Seeded {len(MEMBERS)} members, "
            f"{len(WORKOUT_SESSIONS)} workout sessions, "
            f"{len(EXERCISE_LOGS)} exercise logs, "
            f"{len(NUTRITION_LOGS)} nutrition logs."
        )

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
