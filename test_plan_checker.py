
from plan_checker import check_plan, check_R0


profile = {"age": 25}


# ==========================================
# CREATE A VALID TEST PLAN
# ==========================================

def make_plan():

    muscle_groups = [
        "chest",
        "back",
        "shoulders",
        "biceps",
        "triceps",
        "quads",
        "hamstrings_glutes",
        "calves",
        "core"
    ]

    days = [0, 2, 4]

    plan = []

    for index, day_index in enumerate(days):

        exercises = []

        daily_muscles = muscle_groups[
            index * 3:(index + 1) * 3
        ]

        for muscle in daily_muscles:

            exercises.append({
                "id": f"exercise_{muscle}",
                "primary_muscle": muscle,
                "secondary_muscles": [],
                "equipment": "bodyweight",
                "level": "beginner",
                "sets": 3,
                "minutes_per_set": 3
            })

        plan.append({
            "day_index": day_index,
            "exercises": exercises
        })

    return plan


# ==========================================
# TEST 1: VALID PLAN
# ==========================================

def test_valid_plan():

    plan = make_plan()

    result = check_plan(plan, profile)

    assert result["R0_Age_Eligibility"] is True
    assert result["R1_Equipment"] is True
    assert result["R2_Difficulty"] is True
    assert result["R3_Session_Duration"] is True
    assert result["R4_Muscle_Recovery"] is True
    assert result["R5_No_Repeats"] is True
    assert result["R6_Weekly_Sets"] is True

    assert result["All_Rules_Pass"] is True

    print("Test 1 passed: Valid plan.")


# ==========================================
# TEST 2: R1 - INVALID EQUIPMENT
# ==========================================

def test_R1_equipment():

    plan = make_plan()

    plan[0]["exercises"][0]["equipment"] = "unknown"

    result = check_plan(plan, profile)

    assert result["R1_Equipment"] is False

    print("Test 2 passed: R1 detected invalid equipment.")


# ==========================================
# TEST 3: R2 - INVALID DIFFICULTY
# ==========================================

def test_R2_difficulty():

    plan = make_plan()

    plan[0]["exercises"][0]["level"] = "expert"

    result = check_plan(plan, profile)

    assert result["R2_Difficulty"] is False

    print("Test 3 passed: R2 detected invalid difficulty.")


# ==========================================
# TEST 4: R3 - SESSION TIME EXCEEDED
# ==========================================

def test_R3_time():

    plan = make_plan()

    for exercise in plan[0]["exercises"]:

        exercise["minutes_per_set"] = 20

    result = check_plan(plan, profile)

    assert result["R3_Session_Duration"] is False

    print("Test 4 passed: R3 detected excessive session time.")


# ==========================================
# TEST 5: R4 - CONSECUTIVE-DAY OVERLAP
# ==========================================

def test_R4_recovery():

    plan = make_plan()

    # Change Wednesday to Tuesday
    plan[1]["day_index"] = 1

    repeated_exercise = {
        "id": "extra_chest",
        "primary_muscle": "chest",
        "secondary_muscles": [],
        "equipment": "bodyweight",
        "level": "beginner",
        "sets": 3,
        "minutes_per_set": 3
    }

    # Add chest to Tuesday
    plan[1]["exercises"].append(repeated_exercise)

    result = check_plan(plan, profile)

    assert result["R4_Muscle_Recovery"] is False

    print("Test 5 passed: R4 detected consecutive-day overlap.")


# ==========================================
# TEST 6: R5 - REPEATED EXERCISE
# ==========================================

def test_R5_repeated_exercise():

    plan = make_plan()

    repeated_exercise = plan[0]["exercises"][0].copy()

    # Add duplicate to the same day
    plan[0]["exercises"].append(repeated_exercise)

    result = check_plan(plan, profile)

    assert result["R5_No_Repeats"] is False

    print("Test 6 passed: R5 detected repeated exercise.")


# ==========================================
# TEST 7: R6 - WEEKLY SET LIMIT EXCEEDED
# ==========================================

def test_R6_weekly_sets():

    plan = make_plan()

    # Chest now has 7 sets instead of the maximum 6
    plan[0]["exercises"][0]["sets"] = 7

    result = check_plan(plan, profile)

    assert result["R6_Weekly_Sets"] is False

    print("Test 7 passed: R6 detected excessive weekly sets.")


# ==========================================
# TEST 8: R0 - AGE ELIGIBILITY
# ==========================================

def test_R0_age():

    assert check_R0({"age": 16}) is False
    assert check_R0({"age": 25}) is True
    assert check_R0({"age": 65}) is False

    print("Test 8 passed: R0 age eligibility.")


# ==========================================
# RUN ALL TESTS
# ==========================================

if __name__ == "__main__":

    test_valid_plan()
    test_R1_equipment()
    test_R2_difficulty()
    test_R3_time()
    test_R4_recovery()
    test_R5_repeated_exercise()
    test_R6_weekly_sets()
    test_R0_age()

    print("\nAll tests completed successfully!")
