"""
src/core/tools.py - FitMind AI's agentic Tools layer.

Each tool is a plain Python function with a clear, narrow scope (one tool = one clearly-
scoped capability). Every tool here is read-only or a low-stakes simulated action —
safe to call inside the ReAct loop without human confirmation.

Actions (log_workout, set_fitness_goal) are SIMULATED — they log and return a
confirmation string. In a production system these would write to the DB / send
notifications after explicit user approval.
"""

from datetime import datetime

from src.core.vector_store import retrieve
from src.core.rag import format_context
from src.nl2sql.pipeline import answer as nl2sql_answer
import src.core.memory as memory_module

# In-memory session activity log (episodic memory) — everything FitMind AI has done
# in this session is tracked here so the agent can self-report what it took action on.
ACTION_LOG = []


# ---------------------------------------------------------------------------
# Read-only knowledge tools
# ---------------------------------------------------------------------------

def tool_search_knowledge_base(query: str) -> str:
    """Search the fitness & nutrition knowledge base for any narrative/procedural
    information: workout plans, nutrition guidance, supplement advice, injury prevention,
    recovery protocols, exercise technique cues, FAQs, meal plans, and goal-setting tips.
    Read-only."""
    chunks = retrieve(query, top_k=4)
    return format_context(chunks)


def tool_query_fitness_database(question: str) -> str:
    """Query the structured fitness database (members, workout sessions, exercise logs,
    nutrition logs) for precise counts, averages, totals, or comparisons — e.g. 'how
    many sets of squats did Alex do this week', 'average daily calories for Priya last 7
    days', 'which member logged the highest bench press weight'. Use this instead of
    search_knowledge_base whenever the question needs an exact number or an aggregate
    across many records. Read-only."""
    result = nl2sql_answer(question)
    if result.get("error"):
        return f"Could not safely answer from the fitness database: {result['error']}"
    return f"SQL used: {result['sql']}\n\nAnswer: {result['answer']}"


def tool_calculate_macros(
    weight_kg: float,
    goal: str,
    activity_level: str = "moderately_active",
) -> str:
    """Calculate estimated daily macro targets (protein, carbs, fat, calories) based on
    body weight, goal, and activity level.
    goal options: muscle_gain | fat_loss | maintenance
    activity_level options: sedentary | lightly_active | moderately_active | very_active
    Read-only — returns a formatted macro recommendation string."""

    activity_multipliers = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
    }
    multiplier = activity_multipliers.get(activity_level.lower(), 1.55)

    # Rough BMR using a simplified Mifflin-St Jeor (gender-neutral average)
    bmr = 10 * weight_kg + 500  # simplified, gender-neutral approximation
    tdee = bmr * multiplier

    if goal.lower() == "fat_loss":
        target_calories = tdee - 400
        protein_g = round(weight_kg * 2.0)
        fat_g = round(target_calories * 0.25 / 9)
        carbs_g = round((target_calories - protein_g * 4 - fat_g * 9) / 4)
    elif goal.lower() == "muscle_gain":
        target_calories = tdee + 300
        protein_g = round(weight_kg * 2.0)
        fat_g = round(target_calories * 0.25 / 9)
        carbs_g = round((target_calories - protein_g * 4 - fat_g * 9) / 4)
    else:  # maintenance
        target_calories = tdee
        protein_g = round(weight_kg * 1.8)
        fat_g = round(target_calories * 0.30 / 9)
        carbs_g = round((target_calories - protein_g * 4 - fat_g * 9) / 4)

    return (
        f"Estimated daily targets for {weight_kg} kg / {goal} / {activity_level}:\n"
        f"  Calories : {int(target_calories)} kcal\n"
        f"  Protein  : {protein_g} g  ({round(protein_g/weight_kg, 1)} g/kg)\n"
        f"  Carbs    : {carbs_g} g\n"
        f"  Fat      : {fat_g} g\n"
        f"Note: these are starting estimates. Adjust weekly based on scale trend and energy levels."
    )


def tool_calculate_bmi(weight_kg: float, height_cm: float) -> str:
    """Calculate BMI and return the result with a brief interpretation.
    Read-only."""
    if height_cm <= 0 or weight_kg <= 0:
        return "Invalid inputs — weight and height must be positive numbers."
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25.0:
        category = "Normal weight"
    elif bmi < 30.0:
        category = "Overweight"
    elif bmi < 35.0:
        category = "Obese Class I"
    elif bmi < 40.0:
        category = "Obese Class II"
    else:
        category = "Obese Class III"
    return (
        f"BMI: {bmi:.1f} — {category}\n"
        f"(weight: {weight_kg} kg, height: {height_cm} cm)\n"
        f"Note: BMI does not account for muscle mass. A muscular athlete may show 'overweight' "
        f"while having a healthy body fat percentage."
    )


# ---------------------------------------------------------------------------
# Simulated action tools
# ---------------------------------------------------------------------------

def tool_log_workout(exercise: str, sets: int, reps: int, weight_kg: float = 0.0) -> str:
    """Simulated — log a completed exercise set to the session activity log.
    In a real system this would write to the ExerciseLog table. Reversible, low-stakes."""
    ts = datetime.now().strftime("%H:%M:%S")
    entry = f"[{ts}] WORKOUT LOGGED: {exercise} — {sets} sets x {reps} reps @ {weight_kg} kg"
    ACTION_LOG.append(entry)
    return (
        f"Logged: {exercise} — {sets} x {reps} @ {weight_kg} kg. "
        f"Keep it up — consistent logging is the fastest path to spotting progress trends!"
    )


def tool_set_fitness_goal(goal: str, target_date: str = "unspecified") -> str:
    """Simulated — record a fitness goal with an optional target date.
    Reversible, low-stakes."""
    ts = datetime.now().strftime("%H:%M:%S")
    entry = f"[{ts}] GOAL SET — target date {target_date}: {goal}"
    ACTION_LOG.append(entry)
    return (
        f"Goal set: '{goal}' (target: {target_date}). "
        f"Writing it down is step one — now let's break it into weekly milestones!"
    )


def tool_view_activity_log() -> str:
    """View all actions logged so far this session (episodic memory). Read-only."""
    if not ACTION_LOG:
        return "No actions logged yet this session."
    return "\n".join(ACTION_LOG)


# ---------------------------------------------------------------------------
# Long-term memory tools
# ---------------------------------------------------------------------------

def tool_remember_fact(key: str, value: str) -> str:
    """Persist a durable fact to long-term memory — e.g. key='preferred_protein',
    value='whey isolate'. Survives across sessions. Reversible, low-stakes."""
    return memory_module.remember(key, value)


def tool_recall_fact(key: str) -> str:
    """Recall a previously remembered fact by key from long-term memory. Read-only."""
    return memory_module.recall(key)


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

TOOL_REGISTRY = {
    "search_knowledge_base": {
        "fn": tool_search_knowledge_base,
        "description": (
            "Search the fitness & nutrition knowledge base for narrative/procedural information: "
            "workout plans, nutrition guidance, supplement advice, injury prevention, recovery "
            "protocols, exercise technique cues, meal plans, FAQs, and goal-setting guidance. "
            "Read-only."
        ),
        "risk": "none",
        "confirm": False,
    },
    "query_fitness_database": {
        "fn": tool_query_fitness_database,
        "description": (
            "Query the structured fitness database (members, workout_sessions, exercise_logs, "
            "nutrition_logs) for precise counts, totals, averages, or comparisons — e.g. 'how "
            "many squat sets did Alex log this week', 'average protein intake for Priya', 'which "
            "member has the highest bench press weight'. Use this when the question needs an exact "
            "number or aggregate across records. Read-only."
        ),
        "risk": "none",
        "confirm": False,
    },
    "calculate_macros": {
        "fn": tool_calculate_macros,
        "description": (
            "Calculate estimated daily macro targets (calories, protein, carbs, fat) given "
            "weight_kg (float), goal ('muscle_gain'|'fat_loss'|'maintenance'), and optional "
            "activity_level ('sedentary'|'lightly_active'|'moderately_active'|'very_active'). "
            "Read-only."
        ),
        "risk": "none",
        "confirm": False,
    },
    "calculate_bmi": {
        "fn": tool_calculate_bmi,
        "description": (
            "Calculate BMI and return a brief interpretation given weight_kg (float) and "
            "height_cm (float). Read-only."
        ),
        "risk": "none",
        "confirm": False,
    },
    "log_workout": {
        "fn": tool_log_workout,
        "description": (
            "Log a completed exercise to the session activity log. Provide exercise (str), "
            "sets (int), reps (int), and optional weight_kg (float, default 0.0 for bodyweight). "
            "Simulated — reversible, low-stakes."
        ),
        "risk": "low",
        "confirm": False,
    },
    "set_fitness_goal": {
        "fn": tool_set_fitness_goal,
        "description": (
            "Record a fitness goal with an optional target_date (str, e.g. '2024-12-01'). "
            "Simulated — reversible, low-stakes."
        ),
        "risk": "low",
        "confirm": False,
    },
    "view_activity_log": {
        "fn": tool_view_activity_log,
        "description": "View all actions logged so far this session (episodic memory). Read-only.",
        "risk": "none",
        "confirm": False,
    },
    "remember_fact": {
        "fn": tool_remember_fact,
        "description": (
            "Persist a durable fact to long-term memory across sessions. "
            "Provide key (str) and value (str). Reversible, low-stakes."
        ),
        "risk": "low",
        "confirm": False,
    },
    "recall_fact": {
        "fn": tool_recall_fact,
        "description": "Recall a previously remembered fact by key from long-term memory. Read-only.",
        "risk": "none",
        "confirm": False,
    },
}


def tool_descriptions_block() -> str:
    """Formatted block of tool names + descriptions for the ReAct system prompt."""
    lines = []
    for name, spec in TOOL_REGISTRY.items():
        lines.append(f"- {name}({_signature_hint(name)}): {spec['description']}")
    return "\n".join(lines)


def _signature_hint(name: str) -> str:
    hints = {
        "search_knowledge_base": "query",
        "query_fitness_database": "question",
        "calculate_macros": "weight_kg, goal, activity_level='moderately_active'",
        "calculate_bmi": "weight_kg, height_cm",
        "log_workout": "exercise, sets, reps, weight_kg=0.0",
        "set_fitness_goal": "goal, target_date='unspecified'",
        "view_activity_log": "",
        "remember_fact": "key, value",
        "recall_fact": "key",
    }
    return hints.get(name, "")


def run_tool(name: str, **kwargs):
    if name not in TOOL_REGISTRY:
        return f"ERROR: no such tool '{name}'. Available tools: {', '.join(TOOL_REGISTRY.keys())}"
    return TOOL_REGISTRY[name]["fn"](**kwargs)
