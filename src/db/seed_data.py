"""
src/db/seed_data.py - deterministic, hand-authored seed rows for the fitness DB.

Deliberately NOT randomly generated: every benchmark question in sample_queries.md has
exactly one correct answer that can be verified by reading this file directly. Member
names match data/documents/member_profiles.json so the structured and unstructured
stories stay consistent (e.g. Alex Rivera's squat history in exercise_logs matches his
intermediate profile in the knowledge base).
"""

MEMBERS = [
    {"name": "Alex Rivera",  "age": 28, "sex": "male",   "height_cm": 178, "weight_kg": 82,  "goal": "muscle_gain",          "fitness_level": "intermediate", "dietary_preference": "omnivore"},
    {"name": "Priya Sharma", "age": 34, "sex": "female", "height_cm": 163, "weight_kg": 68,  "goal": "fat_loss",              "fitness_level": "beginner",     "dietary_preference": "vegetarian"},
    {"name": "Jordan Lee",   "age": 22, "sex": "male",   "height_cm": 185, "weight_kg": 75,  "goal": "athletic_performance",  "fitness_level": "intermediate", "dietary_preference": "omnivore"},
    {"name": "Simone Okafor","age": 45, "sex": "female", "height_cm": 170, "weight_kg": 74,  "goal": "general_health",        "fitness_level": "beginner",     "dietary_preference": "vegan"},
    {"name": "Marcus Webb",  "age": 31, "sex": "male",   "height_cm": 181, "weight_kg": 90,  "goal": "muscle_gain",           "fitness_level": "advanced",     "dietary_preference": "omnivore"},
]

# session / member below reference MEMBERS[i]["name"] —
# scripts/seed_db.py resolves these to foreign keys by lookup at insert time.
WORKOUT_SESSIONS = [
    # Alex Rivera — Upper/Lower 4x/week
    {"member": "Alex Rivera",  "session_date": "2024-03-04", "session_type": "strength",  "duration_min": 55, "notes": "Upper A — bench, row, OHP"},
    {"member": "Alex Rivera",  "session_date": "2024-03-05", "session_type": "strength",  "duration_min": 60, "notes": "Lower A — squat, RDL, leg press"},
    {"member": "Alex Rivera",  "session_date": "2024-03-07", "session_type": "strength",  "duration_min": 50, "notes": "Upper B — volume day"},
    {"member": "Alex Rivera",  "session_date": "2024-03-08", "session_type": "strength",  "duration_min": 65, "notes": "Lower B — deadlift focus"},
    {"member": "Alex Rivera",  "session_date": "2024-03-11", "session_type": "strength",  "duration_min": 55, "notes": "Upper A — bench PR attempt"},
    {"member": "Alex Rivera",  "session_date": "2024-03-12", "session_type": "strength",  "duration_min": 60, "notes": "Lower A"},
    {"member": "Alex Rivera",  "session_date": "2024-03-14", "session_type": "strength",  "duration_min": 50, "notes": "Upper B"},
    {"member": "Alex Rivera",  "session_date": "2024-03-15", "session_type": "strength",  "duration_min": 65, "notes": "Lower B"},
    # Priya Sharma — Full-Body 3x/week
    {"member": "Priya Sharma", "session_date": "2024-03-04", "session_type": "full_body", "duration_min": 40, "notes": "Session A"},
    {"member": "Priya Sharma", "session_date": "2024-03-06", "session_type": "full_body", "duration_min": 38, "notes": "Session B"},
    {"member": "Priya Sharma", "session_date": "2024-03-09", "session_type": "full_body", "duration_min": 42, "notes": "Session A"},
    {"member": "Priya Sharma", "session_date": "2024-03-11", "session_type": "full_body", "duration_min": 40, "notes": "Session B"},
    {"member": "Priya Sharma", "session_date": "2024-03-13", "session_type": "cardio",    "duration_min": 30, "notes": "Zone 2 walk/jog"},
    # Jordan Lee — PPL 5x/week (modified, no OHP)
    {"member": "Jordan Lee",   "session_date": "2024-03-04", "session_type": "strength",  "duration_min": 70, "notes": "Push day — no OHP, extra delt work"},
    {"member": "Jordan Lee",   "session_date": "2024-03-05", "session_type": "strength",  "duration_min": 65, "notes": "Pull day"},
    {"member": "Jordan Lee",   "session_date": "2024-03-06", "session_type": "strength",  "duration_min": 75, "notes": "Legs day"},
    {"member": "Jordan Lee",   "session_date": "2024-03-08", "session_type": "hiit",      "duration_min": 25, "notes": "Sprint intervals 10x30s"},
    {"member": "Jordan Lee",   "session_date": "2024-03-09", "session_type": "strength",  "duration_min": 70, "notes": "Push day"},
    {"member": "Jordan Lee",   "session_date": "2024-03-11", "session_type": "strength",  "duration_min": 65, "notes": "Pull day"},
    {"member": "Jordan Lee",   "session_date": "2024-03-12", "session_type": "strength",  "duration_min": 75, "notes": "Legs day"},
    # Simone Okafor — Full-Body 3x/week + Zone 2
    {"member": "Simone Okafor","session_date": "2024-03-04", "session_type": "full_body", "duration_min": 35, "notes": "Session A — form focus"},
    {"member": "Simone Okafor","session_date": "2024-03-06", "session_type": "cardio",    "duration_min": 30, "notes": "Zone 2 cycling"},
    {"member": "Simone Okafor","session_date": "2024-03-07", "session_type": "full_body", "duration_min": 35, "notes": "Session B"},
    {"member": "Simone Okafor","session_date": "2024-03-09", "session_type": "cardio",    "duration_min": 30, "notes": "Zone 2 walk"},
    {"member": "Simone Okafor","session_date": "2024-03-11", "session_type": "full_body", "duration_min": 40, "notes": "Session A — added goblet squat weight"},
    {"member": "Simone Okafor","session_date": "2024-03-13", "session_type": "cardio",    "duration_min": 30, "notes": "Zone 2 cycling"},
    # Marcus Webb — PPL 6x/week (off-season bulk)
    {"member": "Marcus Webb",  "session_date": "2024-03-04", "session_type": "strength",  "duration_min": 80, "notes": "Push — heavy bench focus"},
    {"member": "Marcus Webb",  "session_date": "2024-03-05", "session_type": "strength",  "duration_min": 75, "notes": "Pull — weighted pull-ups"},
    {"member": "Marcus Webb",  "session_date": "2024-03-06", "session_type": "strength",  "duration_min": 85, "notes": "Legs — squat 5x5"},
    {"member": "Marcus Webb",  "session_date": "2024-03-07", "session_type": "strength",  "duration_min": 80, "notes": "Push — volume"},
    {"member": "Marcus Webb",  "session_date": "2024-03-08", "session_type": "strength",  "duration_min": 75, "notes": "Pull — row focus"},
    {"member": "Marcus Webb",  "session_date": "2024-03-09", "session_type": "strength",  "duration_min": 85, "notes": "Legs — deadlift heavy"},
    {"member": "Marcus Webb",  "session_date": "2024-03-11", "session_type": "strength",  "duration_min": 80, "notes": "Push — bench PR"},
    {"member": "Marcus Webb",  "session_date": "2024-03-12", "session_type": "strength",  "duration_min": 75, "notes": "Pull"},
    {"member": "Marcus Webb",  "session_date": "2024-03-13", "session_type": "strength",  "duration_min": 85, "notes": "Legs"},
]

# session references WORKOUT_SESSIONS by index (session_date + member combo) —
# scripts/seed_db.py resolves these to foreign-key session IDs at insert time.
EXERCISE_LOGS = [
    # Alex Rivera — Lower A (2024-03-05)
    {"session": ("Alex Rivera", "2024-03-05"), "exercise_name": "Back Squat",            "sets_completed": 4, "reps_per_set": 7,  "weight_kg": 100, "rpe": 8.0},
    {"session": ("Alex Rivera", "2024-03-05"), "exercise_name": "Romanian Deadlift",     "sets_completed": 3, "reps_per_set": 9,  "weight_kg": 80,  "rpe": 7.5},
    {"session": ("Alex Rivera", "2024-03-05"), "exercise_name": "Leg Press",             "sets_completed": 3, "reps_per_set": 12, "weight_kg": 140, "rpe": 7.0},
    {"session": ("Alex Rivera", "2024-03-05"), "exercise_name": "Leg Curl",              "sets_completed": 3, "reps_per_set": 12, "weight_kg": 40,  "rpe": 7.0},
    {"session": ("Alex Rivera", "2024-03-05"), "exercise_name": "Calf Raise",            "sets_completed": 4, "reps_per_set": 15, "weight_kg": 60,  "rpe": 6.0},
    # Alex Rivera — Upper A (2024-03-04)
    {"session": ("Alex Rivera", "2024-03-04"), "exercise_name": "Bench Press",           "sets_completed": 4, "reps_per_set": 7,  "weight_kg": 80,  "rpe": 8.0},
    {"session": ("Alex Rivera", "2024-03-04"), "exercise_name": "Barbell Row",           "sets_completed": 4, "reps_per_set": 7,  "weight_kg": 75,  "rpe": 8.0},
    {"session": ("Alex Rivera", "2024-03-04"), "exercise_name": "Overhead Press",        "sets_completed": 3, "reps_per_set": 9,  "weight_kg": 50,  "rpe": 7.5},
    {"session": ("Alex Rivera", "2024-03-04"), "exercise_name": "Cable Row",             "sets_completed": 3, "reps_per_set": 12, "weight_kg": 55,  "rpe": 7.0},
    # Alex Rivera — Lower B (2024-03-08)
    {"session": ("Alex Rivera", "2024-03-08"), "exercise_name": "Deadlift",              "sets_completed": 3, "reps_per_set": 5,  "weight_kg": 140, "rpe": 8.5},
    {"session": ("Alex Rivera", "2024-03-08"), "exercise_name": "Back Squat",            "sets_completed": 3, "reps_per_set": 10, "weight_kg": 90,  "rpe": 7.0},
    {"session": ("Alex Rivera", "2024-03-08"), "exercise_name": "Bulgarian Split Squat", "sets_completed": 3, "reps_per_set": 10, "weight_kg": 20,  "rpe": 8.0},
    {"session": ("Alex Rivera", "2024-03-08"), "exercise_name": "Leg Curl",              "sets_completed": 4, "reps_per_set": 12, "weight_kg": 40,  "rpe": 7.0},
    # Alex Rivera — Lower A (2024-03-12, 2.5kg progression)
    {"session": ("Alex Rivera", "2024-03-12"), "exercise_name": "Back Squat",            "sets_completed": 4, "reps_per_set": 7,  "weight_kg": 102.5, "rpe": 8.0},
    {"session": ("Alex Rivera", "2024-03-12"), "exercise_name": "Romanian Deadlift",     "sets_completed": 3, "reps_per_set": 9,  "weight_kg": 82.5,  "rpe": 7.5},
    # Priya Sharma — Full-Body Session A (2024-03-04)
    {"session": ("Priya Sharma","2024-03-04"), "exercise_name": "Goblet Squat",          "sets_completed": 3, "reps_per_set": 12, "weight_kg": 12,  "rpe": 6.5},
    {"session": ("Priya Sharma","2024-03-04"), "exercise_name": "Push-Up",               "sets_completed": 3, "reps_per_set": 10, "weight_kg": 0,   "rpe": 6.0},
    {"session": ("Priya Sharma","2024-03-04"), "exercise_name": "Dumbbell Row",          "sets_completed": 3, "reps_per_set": 12, "weight_kg": 8,   "rpe": 6.0},
    {"session": ("Priya Sharma","2024-03-04"), "exercise_name": "Romanian Deadlift",     "sets_completed": 3, "reps_per_set": 12, "weight_kg": 20,  "rpe": 6.5},
    {"session": ("Priya Sharma","2024-03-04"), "exercise_name": "Plank",                 "sets_completed": 3, "reps_per_set": 1,  "weight_kg": 0,   "rpe": 5.0},
    # Priya Sharma — Full-Body Session B (2024-03-06)
    {"session": ("Priya Sharma","2024-03-06"), "exercise_name": "Leg Press",             "sets_completed": 3, "reps_per_set": 12, "weight_kg": 40,  "rpe": 6.5},
    {"session": ("Priya Sharma","2024-03-06"), "exercise_name": "Incline DB Press",      "sets_completed": 3, "reps_per_set": 10, "weight_kg": 8,   "rpe": 6.0},
    {"session": ("Priya Sharma","2024-03-06"), "exercise_name": "Lat Pulldown",          "sets_completed": 3, "reps_per_set": 12, "weight_kg": 30,  "rpe": 6.5},
    # Jordan Lee — Push Day (2024-03-04)
    {"session": ("Jordan Lee",  "2024-03-04"), "exercise_name": "Bench Press",           "sets_completed": 4, "reps_per_set": 6,  "weight_kg": 90,  "rpe": 8.5},
    {"session": ("Jordan Lee",  "2024-03-04"), "exercise_name": "Incline DB Press",      "sets_completed": 3, "reps_per_set": 10, "weight_kg": 30,  "rpe": 7.5},
    {"session": ("Jordan Lee",  "2024-03-04"), "exercise_name": "Cable Flye",            "sets_completed": 3, "reps_per_set": 15, "weight_kg": 12,  "rpe": 7.0},
    {"session": ("Jordan Lee",  "2024-03-04"), "exercise_name": "Lateral Raise",         "sets_completed": 4, "reps_per_set": 18, "weight_kg": 8,   "rpe": 7.0},
    # Jordan Lee — Legs (2024-03-06)
    {"session": ("Jordan Lee",  "2024-03-06"), "exercise_name": "Back Squat",            "sets_completed": 4, "reps_per_set": 6,  "weight_kg": 110, "rpe": 8.5},
    {"session": ("Jordan Lee",  "2024-03-06"), "exercise_name": "Romanian Deadlift",     "sets_completed": 3, "reps_per_set": 9,  "weight_kg": 85,  "rpe": 7.5},
    {"session": ("Jordan Lee",  "2024-03-06"), "exercise_name": "Leg Press",             "sets_completed": 3, "reps_per_set": 15, "weight_kg": 150, "rpe": 7.0},
    {"session": ("Jordan Lee",  "2024-03-06"), "exercise_name": "Hip Thrust",            "sets_completed": 3, "reps_per_set": 12, "weight_kg": 80,  "rpe": 7.5},
    # Marcus Webb — Squat day (2024-03-06)
    {"session": ("Marcus Webb", "2024-03-06"), "exercise_name": "Back Squat",            "sets_completed": 5, "reps_per_set": 5,  "weight_kg": 150, "rpe": 8.5},
    {"session": ("Marcus Webb", "2024-03-06"), "exercise_name": "Leg Press",             "sets_completed": 3, "reps_per_set": 15, "weight_kg": 220, "rpe": 7.5},
    {"session": ("Marcus Webb", "2024-03-06"), "exercise_name": "Bulgarian Split Squat", "sets_completed": 3, "reps_per_set": 10, "weight_kg": 40,  "rpe": 8.0},
    {"session": ("Marcus Webb", "2024-03-06"), "exercise_name": "Leg Curl",              "sets_completed": 4, "reps_per_set": 12, "weight_kg": 60,  "rpe": 7.0},
    # Marcus Webb — Deadlift day (2024-03-09)
    {"session": ("Marcus Webb", "2024-03-09"), "exercise_name": "Deadlift",              "sets_completed": 4, "reps_per_set": 4,  "weight_kg": 200, "rpe": 9.0},
    {"session": ("Marcus Webb", "2024-03-09"), "exercise_name": "Romanian Deadlift",     "sets_completed": 3, "reps_per_set": 8,  "weight_kg": 120, "rpe": 7.5},
    # Marcus Webb — Push PR day (2024-03-11)
    {"session": ("Marcus Webb", "2024-03-11"), "exercise_name": "Bench Press",           "sets_completed": 5, "reps_per_set": 5,  "weight_kg": 130, "rpe": 9.0},
    {"session": ("Marcus Webb", "2024-03-11"), "exercise_name": "Incline DB Press",      "sets_completed": 3, "reps_per_set": 10, "weight_kg": 50,  "rpe": 8.0},
    {"session": ("Marcus Webb", "2024-03-11"), "exercise_name": "Cable Flye",            "sets_completed": 3, "reps_per_set": 15, "weight_kg": 18,  "rpe": 7.0},
]

NUTRITION_LOGS = [
    # Alex Rivera — muscle gain target ~3000 kcal, ~200g protein
    {"member": "Alex Rivera",  "log_date": "2024-03-04", "calories_kcal": 3050, "protein_g": 198, "carbs_g": 340, "fat_g": 88,  "water_ml": 3200, "notes": "Felt good — hit macros"},
    {"member": "Alex Rivera",  "log_date": "2024-03-05", "calories_kcal": 3120, "protein_g": 205, "carbs_g": 355, "fat_g": 90,  "water_ml": 3400, "notes": "Training day — extra carbs post-workout"},
    {"member": "Alex Rivera",  "log_date": "2024-03-06", "calories_kcal": 2850, "protein_g": 192, "carbs_g": 310, "fat_g": 85,  "water_ml": 2800, "notes": "Rest day — slightly under"},
    {"member": "Alex Rivera",  "log_date": "2024-03-07", "calories_kcal": 3010, "protein_g": 200, "carbs_g": 338, "fat_g": 87,  "water_ml": 3100, "notes": "On track"},
    {"member": "Alex Rivera",  "log_date": "2024-03-08", "calories_kcal": 3150, "protein_g": 210, "carbs_g": 358, "fat_g": 92,  "water_ml": 3500, "notes": "Deadlift day — hungry after"},
    # Priya Sharma — fat loss target ~1750 kcal, ~140g protein
    {"member": "Priya Sharma", "log_date": "2024-03-04", "calories_kcal": 1740, "protein_g": 138, "carbs_g": 185, "fat_g": 52,  "water_ml": 2200, "notes": "Good adherence"},
    {"member": "Priya Sharma", "log_date": "2024-03-05", "calories_kcal": 1680, "protein_g": 132, "carbs_g": 175, "fat_g": 50,  "water_ml": 2100, "notes": "Slightly under — not very hungry"},
    {"member": "Priya Sharma", "log_date": "2024-03-06", "calories_kcal": 1790, "protein_g": 140, "carbs_g": 192, "fat_g": 55,  "water_ml": 2300, "notes": "Training day, added banana pre-workout"},
    {"member": "Priya Sharma", "log_date": "2024-03-07", "calories_kcal": 1650, "protein_g": 128, "carbs_g": 170, "fat_g": 49,  "water_ml": 2000, "notes": "Work event — made best choices available"},
    # Jordan Lee — maintenance/performance ~2600 kcal, ~185g protein
    {"member": "Jordan Lee",   "log_date": "2024-03-04", "calories_kcal": 2620, "protein_g": 188, "carbs_g": 295, "fat_g": 72,  "water_ml": 3600, "notes": "Push day fuelling"},
    {"member": "Jordan Lee",   "log_date": "2024-03-05", "calories_kcal": 2550, "protein_g": 180, "carbs_g": 285, "fat_g": 70,  "water_ml": 3400, "notes": "Pull day — slightly under on carbs"},
    {"member": "Jordan Lee",   "log_date": "2024-03-06", "calories_kcal": 2700, "protein_g": 195, "carbs_g": 310, "fat_g": 74,  "water_ml": 3800, "notes": "Leg day — carb loaded"},
    # Simone Okafor — general health target ~2000 kcal, ~120g protein (vegan)
    {"member": "Simone Okafor","log_date": "2024-03-04", "calories_kcal": 1980, "protein_g": 115, "carbs_g": 260, "fat_g": 68,  "water_ml": 2500, "notes": "Good vegan day"},
    {"member": "Simone Okafor","log_date": "2024-03-06", "calories_kcal": 2020, "protein_g": 122, "carbs_g": 265, "fat_g": 70,  "water_ml": 2600, "notes": "Added hemp seeds to smoothie — protein up"},
    {"member": "Simone Okafor","log_date": "2024-03-07", "calories_kcal": 1950, "protein_g": 112, "carbs_g": 255, "fat_g": 65,  "water_ml": 2400, "notes": "Slightly under protein — remind to add tofu"},
    # Marcus Webb — off-season bulk ~3500 kcal, ~230g protein
    {"member": "Marcus Webb",  "log_date": "2024-03-04", "calories_kcal": 3520, "protein_g": 232, "carbs_g": 410, "fat_g": 98,  "water_ml": 4000, "notes": "Push day — clean bulk"},
    {"member": "Marcus Webb",  "log_date": "2024-03-05", "calories_kcal": 3480, "protein_g": 228, "carbs_g": 402, "fat_g": 96,  "water_ml": 3900, "notes": "Pull day"},
    {"member": "Marcus Webb",  "log_date": "2024-03-06", "calories_kcal": 3600, "protein_g": 240, "carbs_g": 425, "fat_g": 100, "water_ml": 4200, "notes": "Squat day — hungry — extra serving rice"},
    {"member": "Marcus Webb",  "log_date": "2024-03-07", "calories_kcal": 3450, "protein_g": 225, "carbs_g": 398, "fat_g": 95,  "water_ml": 3800, "notes": "Push day — good"},
    {"member": "Marcus Webb",  "log_date": "2024-03-08", "calories_kcal": 3530, "protein_g": 234, "carbs_g": 412, "fat_g": 97,  "water_ml": 4100, "notes": "Pull day"},
    {"member": "Marcus Webb",  "log_date": "2024-03-09", "calories_kcal": 3650, "protein_g": 245, "carbs_g": 430, "fat_g": 102, "water_ml": 4300, "notes": "Deadlift day — highest calorie day"},
]
