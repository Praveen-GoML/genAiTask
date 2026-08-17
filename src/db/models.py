"""
src/db/models.py - the structured fitness-ops schema: members, workout sessions,
exercise logs, and nutrition logs.

This is the "structured data" counterpart to data/documents/ — the same real-world
facts sometimes belong in a relational DB, because a question like "how many sets of
squats did Alex do last week" needs an exact COUNT, not an LLM eyeballing retrieved
chunks. See src/nl2sql/ for how natural language reaches these tables.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String, nullable=False)          # male | female | other
    height_cm = Column(Numeric, nullable=False)
    weight_kg = Column(Numeric, nullable=False)
    goal = Column(String, nullable=False)         # muscle_gain | fat_loss | athletic_performance | general_health
    fitness_level = Column(String, nullable=False)  # beginner | intermediate | advanced
    dietary_preference = Column(String, nullable=False)  # omnivore | vegetarian | vegan

    workout_sessions = relationship("WorkoutSession", back_populates="member")
    nutrition_logs = relationship("NutritionLog", back_populates="member")


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    session_date = Column(Date, nullable=False)
    session_type = Column(String, nullable=False)   # strength | cardio | hiit | mobility | full_body
    duration_min = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)

    member = relationship("Member", back_populates="workout_sessions")
    exercise_logs = relationship("ExerciseLog", back_populates="session")


class ExerciseLog(Base):
    __tablename__ = "exercise_logs"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("workout_sessions.id"), nullable=False)
    exercise_name = Column(String, nullable=False)
    sets_completed = Column(Integer, nullable=False)
    reps_per_set = Column(Integer, nullable=False)  # target reps (last set may vary)
    weight_kg = Column(Numeric, nullable=False)     # 0 for bodyweight exercises
    rpe = Column(Numeric, nullable=True)            # Rate of Perceived Exertion 1–10

    session = relationship("WorkoutSession", back_populates="exercise_logs")


class NutritionLog(Base):
    __tablename__ = "nutrition_logs"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    log_date = Column(Date, nullable=False)
    calories_kcal = Column(Integer, nullable=False)
    protein_g = Column(Numeric, nullable=False)
    carbs_g = Column(Numeric, nullable=False)
    fat_g = Column(Numeric, nullable=False)
    water_ml = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    member = relationship("Member", back_populates="nutrition_logs")
