
import csv
from pathlib import Path


# --------------------------------------------------
# EXERCISE DIFFICULTY LEVELS
# --------------------------------------------------

LEVELS = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3
}


# --------------------------------------------------
# 1. FILTER EXERCISES BY EXPERIENCE LEVEL
# --------------------------------------------------

def filter_exercises(exercises, profile):

    user_level = LEVELS.get(
        str(profile.get("level", "")).strip().lower(),
        0
    )

    if user_level == 0:
        return []

    filtered = []

    for exercise in exercises:

        difficulty = LEVELS.get(
            str(exercise.get("level", "")).strip().lower(),
            0
        )

        # Reject invalid or higher difficulty levels
        if difficulty == 0 or difficulty > user_level:
            continue

        filtered.append(exercise)

    return filtered


# --------------------------------------------------
# 2. LOAD EXERCISES FROM CSV
# --------------------------------------------------

def load_exercises():

    file_path = Path(__file__).parent / "exercises_v1.csv"

    # Check whether the CSV file exists
    if not file_path.exists():
        raise FileNotFoundError(
            f"Exercise dataset not found: {file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        # Required CSV columns
        required_columns = {
            "id",
            "name",
            "primary_muscle",
            "secondary_muscles",
            "equipment",
            "level",
            "minutes_per_set"
        }

        actual_columns = set(reader.fieldnames or [])

        missing_columns = required_columns - actual_columns

        if missing_columns:
            raise ValueError(
                "Missing CSV columns: "
                + ", ".join(sorted(missing_columns))
            )

        exercises = list(reader)

    if not exercises:
        raise ValueError("The exercise dataset is empty.")

    return exercises


# --------------------------------------------------
# 3. TEST EXERCISE FILTER
# --------------------------------------------------

if __name__ == "__main__":

    profile = {
        "level": "beginner"
    }

    try:

        exercises = load_exercises()

        filtered = filter_exercises(
            exercises,
            profile
        )

        print("\n========== EXERCISE FILTER TEST ==========")

        print("Total exercises:", len(exercises))

        print("Suitable exercises:", len(filtered))

        print("\nFiltered Exercises:\n")

        for exercise in filtered:

            print(
                exercise["name"],
                "| Level:", exercise["level"],
                "| Muscle:", exercise["primary_muscle"]
            )

    except (FileNotFoundError, ValueError) as error:

        print("\nError:", error)
