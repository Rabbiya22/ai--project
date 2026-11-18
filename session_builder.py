
import heapq
from itertools import count

from exercise_filter import load_exercises, filter_exercises
from weekly_split import dfs_split, DAY_NAMES, MUSCLE_GROUPS

from plan_checker import (
    check_R0,
    get_age_message,
    check_plan,
    MAX_SESSION_MINUTES,
    ALLOWED_EQUIPMENT
)


# ==================================================
# PROJECT SETTINGS
# ==================================================

SETS = 3
PROJECT_LEVEL = "beginner"
PROJECT_EQUIPMENT = ALLOWED_EQUIPMENT

LEVEL_RANK = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3
}

# These names MUST match plan_checker.py exactly.
RULE_NAMES = [
    "R0_Age_Eligibility",
    "R1_Equipment",
    "R2_Difficulty",
    "R3_Session_Duration",
    "R4_Muscle_Recovery",
    "R5_No_Repeats",
    "R6_Weekly_Sets"
]


# ==================================================
# CUSTOMER PROFILE
# ==================================================

def get_customer_profile():

    while True:
        try:
            age = int(input("Enter your age: "))

            profile = {
                "age": age,
                "level": PROJECT_LEVEL,
                "equipment": PROJECT_EQUIPMENT,
                "session_minutes": MAX_SESSION_MINUTES
            }

            if not check_R0(profile):
                print(get_age_message(age))
                continue

            return profile

        except ValueError:
            print("Please enter a valid whole-number age.")


# ==================================================
# USER AVAILABILITY
# ==================================================

def get_user_availability():

    print("\nChoose your preferred workout days.")
    print("0 = Monday")
    print("1 = Tuesday")
    print("2 = Wednesday")
    print("3 = Thursday")
    print("4 = Friday")
    print("5 = Saturday")
    print("Sunday is closed.")

    while True:
        try:
            entered_days = input(
                "\nEnter day numbers separated by commas: "
            )

            preferred_days = [
                int(day.strip())
                for day in entered_days.split(",")
            ]

            if not 1 <= len(preferred_days) <= 6:
                print("Please select between 1 and 6 days.")
                continue
            if not 2 <= len(preferred_days) <= 6:
                print("Please select between 2 and 6 days.")
                continue
            if len(set(preferred_days)) != len(preferred_days):
                print("You cannot select the same day twice.")
                continue

            if any(day < 0 or day > 5 for day in preferred_days):
                print("Choose days from 0 to 5 only.")
                continue

            return sorted(preferred_days)

        except ValueError:
            print("Enter valid day numbers separated by commas.")


# ==================================================
# VALIDATE DATASET IDS
# ==================================================

def validate_unique_ids(exercises):

    seen_ids = set()

    for exercise in exercises:

        exercise_id = str(
            exercise.get("id", "")
        ).strip()

        if not exercise_id:
            raise ValueError("An exercise is missing its ID.")

        if exercise_id in seen_ids:
            raise ValueError(
                f"Duplicate exercise ID found: {exercise_id}"
            )

        seen_ids.add(exercise_id)

    return True


# ==================================================
# PREPARE EXERCISE DATA
# ==================================================

def prepare_exercise(exercise):

    primary = str(
        exercise.get("primary_muscle", "")
    ).strip().lower()

    secondary = exercise.get("secondary_muscles", "")

    if isinstance(secondary, str):
        secondary = secondary.replace(",", ";").split(";")

    secondary = [
        muscle.strip().lower()
        for muscle in secondary
        if muscle.strip()
    ]

    try:
        minutes = float(
            exercise.get("minutes_per_set", 0)
        )
    except (ValueError, TypeError):
        minutes = 0

    prepared = exercise.copy()

    prepared["id"] = str(
        exercise.get("id", "")
    ).strip()

    prepared["name"] = str(
        exercise.get("name", "")
    ).strip()

    prepared["primary_muscle"] = primary
    prepared["secondary_muscles"] = secondary

    prepared["equipment"] = str(
        exercise.get("equipment", "")
    ).strip().lower()

    prepared["level"] = str(
        exercise.get("level", "")
    ).strip().lower()

    prepared["minutes_per_set"] = minutes
    prepared["sets"] = SETS

    return prepared


# ==================================================
# CHECK EXERCISE SUITABILITY
# ==================================================

def is_suitable_exercise(exercise, profile):

    equipment = exercise["equipment"]
    level = exercise["level"]
    minutes = exercise["minutes_per_set"]

    if equipment not in PROJECT_EQUIPMENT:
        return False

    if level not in LEVEL_RANK:
        return False

    if LEVEL_RANK[level] > LEVEL_RANK[profile["level"]]:
        return False

    if minutes <= 0:
        return False

    if not exercise["id"] or not exercise["name"]:
        return False

    if exercise["primary_muscle"] not in MUSCLE_GROUPS:
        return False

    return True


# ==================================================
# GET PRIMARY AND SECONDARY MUSCLES
# ==================================================

def get_active_muscles(exercise):

    active = set()

    primary = exercise.get("primary_muscle", "")

    if primary:
        active.add(primary.strip().lower())

    secondary = exercise.get("secondary_muscles", [])

    if isinstance(secondary, str):
        secondary = secondary.replace(",", ";").split(";")

    for muscle in secondary:
        muscle = muscle.strip().lower()

        if muscle:
            active.add(muscle)

    return active


# ==================================================
# CALCULATE EXERCISE TIME
# ==================================================

def exercise_time(exercise):

    return (
        exercise["minutes_per_set"] *
        exercise["sets"]
    )


# ==================================================
# A* SESSION BUILDER
# ==================================================

def build_session(
    target_muscles,
    suitable_exercises,
    blocked_muscles
):

    candidates = {}

    for muscle in target_muscles:

        candidates[muscle] = [
            exercise
            for exercise in suitable_exercises
            if exercise["primary_muscle"] == muscle
            and get_active_muscles(exercise).isdisjoint(
                blocked_muscles
            )
        ]

        if not candidates[muscle]:
            return None

    minimum_times = []

    for muscle in target_muscles:

        minimum_time = min(
            exercise_time(exercise)
            for exercise in candidates[muscle]
        )

        minimum_times.append(minimum_time)

    # A* heuristic
    heuristic = [0] * (len(target_muscles) + 1)

    for index in range(len(target_muscles) - 1, -1, -1):

        heuristic[index] = (
            heuristic[index + 1] +
            minimum_times[index]
        )

    priority_queue = []
    tie_breaker = count()

    heapq.heappush(
        priority_queue,
        (
            heuristic[0],
            0,
            next(tie_breaker),
            0,
            []
        )
    )

    while priority_queue:

        (
            estimated_total,
            total_time,
            _,
            index,
            selected
        ) = heapq.heappop(priority_queue)

        if index == len(target_muscles):

            if total_time <= MAX_SESSION_MINUTES:
                return selected

            continue

        muscle = target_muscles[index]

        for exercise in candidates[muscle]:

            exercise_id = exercise["id"]

            selected_ids = {
                item["id"] for item in selected
            }

            if exercise_id in selected_ids:
                continue

            new_time = (
                total_time + exercise_time(exercise)
            )

            if new_time > MAX_SESSION_MINUTES:
                continue

            new_selected = selected + [exercise]

            new_estimate = (
                new_time + heuristic[index + 1]
            )

            heapq.heappush(
                priority_queue,
                (
                    new_estimate,
                    new_time,
                    next(tie_breaker),
                    index + 1,
                    new_selected
                )
            )

    return None


# ==================================================
# DISPLAY WEEKLY SET TOTALS
# ==================================================

def show_weekly_sets(plan):

    weekly_sets = {
        muscle: 0
        for muscle in MUSCLE_GROUPS
    }

    for day in plan:

        for exercise in day["exercises"]:

            muscle = exercise["primary_muscle"]
            sets = exercise["sets"]

            if muscle in weekly_sets:
                weekly_sets[muscle] += sets

    print("\nWEEKLY SET TOTALS")

    for muscle, total in weekly_sets.items():
        print(f"{muscle}: {total} sets")

    return weekly_sets


# ==================================================
# DISPLAY GENERATED PLAN
# ==================================================

def display_plan(plan):

    print("\n" + "=" * 45)
    print("GENERATED WEEKLY WORKOUT PLAN")
    print("=" * 45)

    for day in plan:

        day_name = DAY_NAMES[day["day_index"]]

        print(f"\n{day_name}")

        total_time = 0

        for exercise in day["exercises"]:

            duration = exercise_time(exercise)
            total_time += duration

            print(
                f"- {exercise['name']} "
                f"({exercise['sets']} sets, "
                f"{duration:g} minutes)"
            )

        print(
            f"Total session time: {total_time:g} minutes"
        )


# ==================================================
# FINAL RULE VALIDATION
# ==================================================

def validate_final_plan(generated_plan, profile):

    print("\n" + "=" * 45)
    print("FINAL RULE VALIDATION")
    print("=" * 45)

    result = check_plan(generated_plan, profile)

    all_rules_pass = True

    for rule in RULE_NAMES:

        status = result.get(rule)

        if status is True:
            print(f"{rule}: PASS")

        elif status is False:
            print(f"{rule}: FAIL")
            all_rules_pass = False

        else:
            print(f"{rule}: NOT CHECKED")
            all_rules_pass = False

    print("\n" + "=" * 45)

    if all_rules_pass:
        print("FINAL RESULT: PLAN APPROVED")
    else:
        print("FINAL RESULT: PLAN NOT APPROVED")

    print("=" * 45)

    return all_rules_pass


# ==================================================
# MAIN PROGRAM
# ==================================================

def main():

    print("=" * 45)
    print("AI WORKOUT PLANNER")
    print("=" * 45)

    # 1. Get customer profile
    profile = get_customer_profile()

    # 2. Get preferred workout days
    preferred_days = get_user_availability()

    # 3. Load exercise dataset
    try:

        raw_exercises = load_exercises()

        if not raw_exercises:
            print("The exercise dataset is empty.")
            return

        validate_unique_ids(raw_exercises)

    except (FileNotFoundError, ValueError) as error:

        print("Dataset error:", error)
        return

    print(
        f"\nTotal exercises in dataset: "
        f"{len(raw_exercises)}"
    )

    # 4. Filter exercises by project level
    filtered_exercises = filter_exercises(
        raw_exercises,
        profile
    )

    # 5. Prepare and validate exercise data
    suitable_exercises = []

    for exercise in filtered_exercises:

        prepared = prepare_exercise(exercise)

        if is_suitable_exercise(prepared, profile):
            suitable_exercises.append(prepared)

    print(
        f"Suitable beginner exercises: "
        f"{len(suitable_exercises)}"
    )

    if not suitable_exercises:
        print("No suitable exercises were found.")
        return

    # 6. Generate weekly muscle split using DFS
    weekly_split = dfs_split(
        len(preferred_days),
        preferred_days
    )

    if weekly_split is None:
        print("DFS could not create a weekly split.")
        return

    print("\nDFS WEEKLY MUSCLE SPLIT")

    for day, muscles in weekly_split.items():

        print(
            f"{DAY_NAMES[day]}: "
            f"{', '.join(muscles)}"
        )

    # 7. Generate daily sessions using A*
    generated_plan = []
    active_by_day = {}

    for day in sorted(weekly_split):

        blocked_muscles = active_by_day.get(
            day - 1,
            set()
        )

        target_muscles = weekly_split[day]

        selected_exercises = build_session(
            target_muscles,
            suitable_exercises,
            blocked_muscles
        )

        if selected_exercises is None:

            print(
                f"\nCould not build a valid session "
                f"for {DAY_NAMES[day]}."
            )

            print("The weekly plan cannot be approved.")
            return

        day_active_muscles = set()

        for exercise in selected_exercises:
            day_active_muscles.update(
                get_active_muscles(exercise)
            )

        active_by_day[day] = day_active_muscles

        generated_plan.append({
            "day_index": day,
            "exercises": selected_exercises
        })

    # 8. Display weekly plan
    display_plan(generated_plan)

    # 9. Display weekly sets
    show_weekly_sets(generated_plan)

    # 10. Validate all rules
    validate_final_plan(
        generated_plan,
        profile
    )


# ==================================================
# RUN PROGRAM
# ==================================================

if __name__ == "__main__":

    try:
        main()

    except (FileNotFoundError, ValueError, KeyError) as error:
        print("\nProgram error:", error)
