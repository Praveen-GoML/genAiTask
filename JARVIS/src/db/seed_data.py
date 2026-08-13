"""
src/db/seed_data.py - deterministic, hand-authored seed rows for the fleet-ops DB.

Deliberately NOT randomly generated: every benchmark question in sample_queries.md has
exactly one correct answer an intern can check the NL2SQL pipeline's generated SQL
against by reading this file directly. A few facts (e.g. the Mark 42's left boot thruster
being flagged 3 times) are kept consistent with data/documents/suit_diagnostics.txt on
purpose, so a curious intern can cross-check the structured and unstructured stories.
"""

SUITS = [
    {"mark_name": "Mark 42", "status": "needs_maintenance", "power_core_pct": 84, "last_diagnostic_date": "2024-03-11"},
    {"mark_name": "Mark 45", "status": "combat_ready", "power_core_pct": 97, "last_diagnostic_date": "2024-03-19"},
    {"mark_name": "Mark 50", "status": "combat_ready", "power_core_pct": 99, "last_diagnostic_date": "2024-03-20"},
    {"mark_name": "War Machine", "status": "combat_ready", "power_core_pct": 91, "last_diagnostic_date": "2024-03-18"},
    {"mark_name": "Rescue", "status": "in_storage", "power_core_pct": 88, "last_diagnostic_date": "2024-02-01"},
    {"mark_name": "Mark 7", "status": "decommissioned", "power_core_pct": 0, "last_diagnostic_date": "2012-05-04"},
]

TECHNICIANS = [
    {"name": "Happy Hogan", "specialty": "Structural", "years_experience": 8},
    {"name": "Tony Stark", "specialty": "Propulsion", "years_experience": 20},
    {"name": "Priya Anand", "specialty": "Avionics", "years_experience": 6},
    {"name": "Dmitri Kovalenko", "specialty": "Power Systems", "years_experience": 11},
    {"name": "Sam Wilkins", "specialty": "Structural", "years_experience": 4},
    {"name": "JARVIS Automated Diagnostics", "specialty": "Software", "years_experience": 0},
]

# suit / technician below reference SUITS[i]["mark_name"] / TECHNICIANS[i]["name"] -
# scripts/seed_db.py resolves these to foreign keys by lookup at insert time.
MAINTENANCE_EVENTS = [
    {"suit": "Mark 42", "technician": "Happy Hogan", "event_date": "2023-12-01", "component": "Left boot thruster", "issue": "Intermittent fault under cold conditions", "resolution": "Replaced thruster coil and resealed housing", "resolution_hours": 4.5, "cost_usd": 2200},
    {"suit": "Mark 42", "technician": "Happy Hogan", "event_date": "2024-01-14", "component": "Left boot thruster", "issue": "Repeat intermittent fault after coil replacement", "resolution": "Escalated to full thruster housing replacement", "resolution_hours": 9, "cost_usd": 6800},
    {"suit": "Mark 42", "technician": "Happy Hogan", "event_date": "2024-03-02", "component": "Left boot thruster", "issue": "Fault flagged a third time under sustained cold exposure", "resolution": "Replaced with redesigned cold-rated coil assembly", "resolution_hours": 6, "cost_usd": 4100},
    {"suit": "Mark 42", "technician": "Priya Anand", "event_date": "2024-02-10", "component": "HUD display", "issue": "Minor glare artifact in direct sunlight", "resolution": "Recalibrated display polarization filter", "resolution_hours": 1.5, "cost_usd": 300},
    {"suit": "Mark 42", "technician": "Dmitri Kovalenko", "event_date": "2024-01-22", "component": "Power core regulator", "issue": "Output dipped 4% below nominal for under a minute", "resolution": "Replaced regulator fuse, retested to spec", "resolution_hours": 2, "cost_usd": 900},
    {"suit": "Mark 42", "technician": "Happy Hogan", "event_date": "2024-03-11", "component": "Right boot thruster", "issue": "New fault reported on right side for the first time", "resolution": "Replaced right thruster coil preemptively", "resolution_hours": 4, "cost_usd": 2100},
    {"suit": "Mark 42", "technician": "Happy Hogan", "event_date": "2024-02-07", "component": "Left gauntlet plating", "issue": "Minor wear from training exercise", "resolution": "Buffed and resealed plating", "resolution_hours": 1, "cost_usd": 150},
    {"suit": "Mark 42", "technician": "Tony Stark", "event_date": "2024-01-20", "component": "Repulsor coil", "issue": "Output 3% below spec on diagnostic sweep", "resolution": "Recalibrated repulsor coil alignment", "resolution_hours": 2, "cost_usd": 500},
    {"suit": "Mark 45", "technician": "Tony Stark", "event_date": "2024-02-03", "component": "Chestplate servo", "issue": "Minor calibration drift after a high-G maneuver", "resolution": "Recalibrated via the diagnostic dock", "resolution_hours": 1, "cost_usd": 150},
    {"suit": "Mark 45", "technician": "Tony Stark", "event_date": "2024-03-19", "component": "Power regulation circuit", "issue": "Output fluctuation of plus or minus 2 percent under sustained load", "resolution": "Replaced the regulation circuit board", "resolution_hours": 3, "cost_usd": 2400},
    {"suit": "Mark 45", "technician": "Sam Wilkins", "event_date": "2023-12-15", "component": "Left gauntlet plating", "issue": "Hairline stress fracture after impact", "resolution": "Replaced plating section", "resolution_hours": 2.5, "cost_usd": 700},
    {"suit": "Mark 45", "technician": "Happy Hogan", "event_date": "2024-03-05", "component": "Chestplate servo", "issue": "Servo grinding noise reported by pilot", "resolution": "Lubricated and retested servo assembly", "resolution_hours": 1, "cost_usd": 180},
    {"suit": "Mark 45", "technician": "Sam Wilkins", "event_date": "2024-01-16", "component": "Chestplate integrity", "issue": "Minor scoring from debris impact", "resolution": "Buffed and resealed chestplate coating", "resolution_hours": 1.5, "cost_usd": 300},
    {"suit": "Mark 45", "technician": "Dmitri Kovalenko", "event_date": "2024-03-15", "component": "Power core regulator", "issue": "Preventive inspection ahead of scheduled mission", "resolution": "No repair needed - logged as passed diagnostic", "resolution_hours": 1, "cost_usd": 0},
    {"suit": "Mark 50", "technician": "JARVIS Automated Diagnostics", "event_date": "2024-02-20", "component": "Nanotech reassembly matrix", "issue": "Reassembly lag of 0.4 seconds above spec", "resolution": "Applied firmware patch; lag reduced to 0.1 seconds", "resolution_hours": 0.5, "cost_usd": 0},
    {"suit": "Mark 50", "technician": "Dmitri Kovalenko", "event_date": "2024-01-05", "component": "Repulsor coil", "issue": "Thermal throttling triggered below spec threshold", "resolution": "Replaced coolant line, retested under load", "resolution_hours": 3, "cost_usd": 1800},
    {"suit": "Mark 50", "technician": "Priya Anand", "event_date": "2023-12-28", "component": "Targeting HUD", "issue": "Lock time drift of 0.1 seconds above spec", "resolution": "Recalibrated sensor array", "resolution_hours": 1, "cost_usd": 200},
    {"suit": "Mark 50", "technician": "Sam Wilkins", "event_date": "2024-02-14", "component": "Left boot thruster", "issue": "Minor efficiency loss reported", "resolution": "Cleaned thruster intake, retested to spec", "resolution_hours": 2, "cost_usd": 400},
    {"suit": "Mark 50", "technician": "Tony Stark", "event_date": "2024-02-28", "component": "Nanotech reassembly matrix", "issue": "Routine firmware audit", "resolution": "Updated firmware to latest validated build", "resolution_hours": 1, "cost_usd": 0},
    {"suit": "Mark 50", "technician": "Priya Anand", "event_date": "2024-03-20", "component": "Power core regulator", "issue": "Routine post-mission inspection", "resolution": "No repair needed - logged as passed diagnostic", "resolution_hours": 0.5, "cost_usd": 0},
    {"suit": "War Machine", "technician": "Happy Hogan", "event_date": "2024-01-30", "component": "Minigun mount", "issue": "Mount vibration exceeding tolerance during sustained fire", "resolution": "Reinforced mount bracket", "resolution_hours": 5, "cost_usd": 3100},
    {"suit": "War Machine", "technician": "Sam Wilkins", "event_date": "2023-11-18", "component": "Left leg actuator", "issue": "Actuator response delay under heavy load", "resolution": "Replaced actuator servo", "resolution_hours": 4, "cost_usd": 2600},
    {"suit": "War Machine", "technician": "Tony Stark", "event_date": "2024-02-25", "component": "Power core regulator", "issue": "Output spike during weapons discharge", "resolution": "Installed surge dampener", "resolution_hours": 3.5, "cost_usd": 2900},
    {"suit": "War Machine", "technician": "Priya Anand", "event_date": "2024-01-27", "component": "Comms array", "issue": "Static interference on priority channel", "resolution": "Replaced comms antenna array", "resolution_hours": 2.5, "cost_usd": 1200},
    {"suit": "War Machine", "technician": "Priya Anand", "event_date": "2023-11-30", "component": "HUD display", "issue": "Refresh rate below spec under G-load", "resolution": "Replaced HUD driver board", "resolution_hours": 2, "cost_usd": 950},
    {"suit": "War Machine", "technician": "Sam Wilkins", "event_date": "2023-12-08", "component": "Flight stabilizer", "issue": "Drift during high-speed maneuvering", "resolution": "Recalibrated stabilizer gyroscope", "resolution_hours": 1.5, "cost_usd": 300},
    {"suit": "Rescue", "technician": "Priya Anand", "event_date": "2023-11-05", "component": "Flight stabilizer", "issue": "Minor drift during hover mode", "resolution": "Recalibrated stabilizer gyroscope", "resolution_hours": 1, "cost_usd": 250},
    {"suit": "Rescue", "technician": "Dmitri Kovalenko", "event_date": "2024-01-08", "component": "Power core", "issue": "Routine capacity check, no fault found", "resolution": "No repair needed - logged as passed diagnostic", "resolution_hours": 0.5, "cost_usd": 0},
    {"suit": "Rescue", "technician": "Dmitri Kovalenko", "event_date": "2023-12-20", "component": "Arc Reactor (chest unit, current)", "issue": "Output ceiling test", "resolution": "No repair needed - logged as passed diagnostic", "resolution_hours": 0.5, "cost_usd": 0},
    {"suit": "Mark 7", "technician": "Tony Stark", "event_date": "2012-05-04", "component": "Full frame", "issue": "Total structural failure during the Battle of New York", "resolution": "Suit decommissioned, not repaired", "resolution_hours": 0, "cost_usd": 0},
]

MISSIONS = [
    {"suit": "Mark 42", "mission_date": "2024-01-05", "location": "Malibu Coastline", "threat_level": 4, "duration_min": 38, "outcome": "success"},
    {"suit": "Mark 42", "mission_date": "2024-02-18", "location": "Downtown LA", "threat_level": 3, "duration_min": 22, "outcome": "success"},
    {"suit": "Mark 42", "mission_date": "2024-03-01", "location": "Pacific Test Range", "threat_level": 2, "duration_min": 15, "outcome": "success"},
    {"suit": "Mark 42", "mission_date": "2023-12-12", "location": "Nevada Desert Range", "threat_level": 2, "duration_min": 14, "outcome": "success"},
    {"suit": "Mark 45", "mission_date": "2024-01-20", "location": "New York City", "threat_level": 5, "duration_min": 54, "outcome": "success"},
    {"suit": "Mark 45", "mission_date": "2024-02-05", "location": "Extremis Containment Site", "threat_level": 5, "duration_min": 61, "outcome": "partial"},
    {"suit": "Mark 45", "mission_date": "2024-03-10", "location": "Stark Industries Perimeter", "threat_level": 2, "duration_min": 12, "outcome": "success"},
    {"suit": "Mark 45", "mission_date": "2024-02-27", "location": "Miami Coastal Patrol", "threat_level": 3, "duration_min": 19, "outcome": "success"},
    {"suit": "Mark 50", "mission_date": "2024-01-12", "location": "Wakanda Border", "threat_level": 5, "duration_min": 47, "outcome": "success"},
    {"suit": "Mark 50", "mission_date": "2024-02-22", "location": "Sokovia Airspace", "threat_level": 5, "duration_min": 58, "outcome": "success"},
    {"suit": "Mark 50", "mission_date": "2024-03-05", "location": "Siberian Facility", "threat_level": 4, "duration_min": 33, "outcome": "success"},
    {"suit": "Mark 50", "mission_date": "2023-12-30", "location": "Test Flight Corridor", "threat_level": 1, "duration_min": 8, "outcome": "success"},
    {"suit": "Mark 50", "mission_date": "2024-01-15", "location": "Arctic Research Station", "threat_level": 4, "duration_min": 36, "outcome": "aborted"},
    {"suit": "War Machine", "mission_date": "2024-01-08", "location": "Wakanda Border", "threat_level": 5, "duration_min": 49, "outcome": "success"},
    {"suit": "War Machine", "mission_date": "2024-02-14", "location": "Lagos", "threat_level": 4, "duration_min": 30, "outcome": "partial"},
    {"suit": "War Machine", "mission_date": "2024-03-18", "location": "USAF Joint Exercise", "threat_level": 2, "duration_min": 20, "outcome": "success"},
    {"suit": "War Machine", "mission_date": "2024-03-22", "location": "Joint NATO Exercise", "threat_level": 3, "duration_min": 28, "outcome": "success"},
    {"suit": "Rescue", "mission_date": "2023-11-10", "location": "Malibu Cliffside Recovery", "threat_level": 3, "duration_min": 25, "outcome": "success"},
    {"suit": "Rescue", "mission_date": "2024-01-25", "location": "Stark Expo Backup", "threat_level": 1, "duration_min": 10, "outcome": "success"},
    {"suit": "Rescue", "mission_date": "2024-02-01", "location": "Stark Tower Perimeter Drill", "threat_level": 1, "duration_min": 9, "outcome": "success"},
]
