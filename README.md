# ai--project
# AI-Based Gym Workout Planner

## 1. Project Overview

The AI-Based Gym Workout Planner is a Python project that automatically generates a weekly workout schedule using Artificial Intelligence search algorithms.

The system takes the user's age and preferred gym days as input. It distributes nine primary muscle groups across the selected days and selects suitable exercises for each session.

The main purpose is to demonstrate how AI search techniques can solve a scheduling and selection problem while following predefined constraints.
members name                    rollno 
Gul e sameen                    281131233
tayyba yahya                    280057658
Rabbiya Asad                    281172264


## 2. Project Objectives

- Generate a weekly workout schedule automatically.
- Distribute nine primary muscle groups across selected days.
- Use DFS for weekly muscle-group distribution.
- Use A* Search for daily exercise selection.
- Keep each session within 45 minutes.
- Consider muscle recovery between consecutive calendar days.
- Avoid repeated exercises within a session.
- Validate the generated plan using seven rules.

## 3. Technologies and Dependencies

- **Programming Language:** Python 3.11
- **Dataset:** CSV file
- **AI Algorithms:** Depth-First Search (DFS) and A* Search
- **Data Structures:** Lists, dictionaries, sets, and priority queues

The project uses Python's standard libraries, including:

- `csv` – reading the exercise dataset.
- `heapq` – managing the A* priority queue.
- `itertools` – supporting combinations where required.

No third-party packages are required by the described implementation.

## 4. Project Structure

```text
workout_planner/
│
├── session_builder.py
├── weekly_split.py
├── exercise_filter.py
├── plan_checker.py
├── test_plan_checker.py
├── exercises_v1.csv
└── README.md
```

### Description of Files

| File | Description |
|---|---|
| `session_builder.py` | Main program. Takes user input and coordinates workout generation. |
| `weekly_split.py` | Uses DFS to distribute muscle groups across selected workout days. |
| `exercise_filter.py` | Filters exercises according to the required difficulty level. |
| `plan_checker.py` | Checks the generated plan against rules R0–R6. |
| `test_plan_checker.py` | Contains unit tests for the plan validation component. |
| `exercises_v1.csv` | Contains the exercise dataset. |

## 5. System Architecture

The system follows these steps:

1. The user enters their age.
2. The system validates the age.
3. The user selects their preferred gym days.
4. The system validates the selected days.
5. DFS distributes the nine primary muscle groups across the selected days.
6. A* selects suitable exercises for each day's assigned muscle groups.
7. The plan checker checks the generated schedule.
8. The system displays the workout plan and validation results.

### Role of DFS

Depth-First Search is used to explore possible weekly muscle-group arrangements.

It distributes the nine primary muscle groups across the available workout days.

### Role of A*

A* Search selects exercises for each day's assigned muscle groups.

It uses the evaluation function:

**f(n) = g(n) + h(n)**

- `g(n)` represents the time spent on selected exercises.
- `h(n)` estimates the minimum time required for the remaining muscle groups.
- `f(n)` represents the estimated total cost of the current search state.

A priority queue is used to explore the most promising states.

## 6. Exercise Dataset

The project uses `exercises_v1.csv`, which contains 120 exercise records.

The dataset includes:

- Exercise ID
- Exercise name
- Primary muscle
- Secondary muscles
- Equipment
- Difficulty level
- Compound exercise information
- Movement type
- Minutes per set
- Goal tags
- Rep range

The system currently uses beginner-level exercises and assumes all five supported equipment categories are available:

- Bodyweight
- Bands and other
- Dumbbell
- Barbell
- Machine and cable

## 7. Project Rules and Constraints

| Rule | Description |
|---|---|
| R0 – Age Eligibility | Age must be between 19 and 59. |
| R1 – Equipment | Exercises must use allowed and available equipment. |
| R2 – Difficulty | Exercise difficulty cannot exceed the user's level. |
| R3 – Session Duration | Each session must not exceed 45 minutes. |
| R4 – Muscle Recovery | Primary and secondary muscles cannot overlap with muscles worked on the previous calendar day. |
| R5 – No Repeats | An exercise ID cannot repeat within the same session. |
| R6 – Weekly Sets | Each primary muscle group must have between 1 and 6 sets across the week. |

### Other Project Settings

- Minimum workout days: 2
- Maximum workout days: 6
- Sunday: Closed
- Sets per exercise: 3
- Maximum session duration: 45 minutes
- Project difficulty level: Beginner

## 8. How to Run the Project

### Step 1: Install Python

Install Python 3.11 or a compatible Python 3 version.

### Step 2: Open the Project Folder

Open the project folder in VS Code or PowerShell.

### Step 3: Run the Main Program

Enter:

```bash
python session_builder.py
```

### Step 4: Enter User Information

The program asks for:

- Age
- Preferred workout days

Day numbers:

| Number | Day |
|---:|---|
| 0 | Monday |
| 1 | Tuesday |
| 2 | Wednesday |
| 3 | Thursday |
| 4 | Friday |
| 5 | Saturday |

For example:

```text
Age: 25
Preferred days: 0,2
```

This selects Monday and Wednesday.

The system then generates the weekly plan and displays the validation results.

## 9. Running Unit Tests

To run the plan checker tests, use:

```bash
python -m unittest test_plan_checker.py
```

The tests cover valid plans and examples of rule violations, including invalid equipment, difficulty, session duration, muscle recovery, repeated exercises, weekly sets, and age eligibility.

## 10. Current Limitations

- The project uses a fixed beginner difficulty level.
- All supported equipment categories are assumed to be available.
- The maximum session duration is fixed at 45 minutes.
- User input is limited mainly to age and preferred gym days.
- The system depends on the exercises available in the CSV dataset.
- The system does not currently save user profiles or previous plans.

## 11. Future Improvements

Possible improvements include:

- Allowing users to select their difficulty level.
- Adding equipment availability as user input.
- Supporting different session durations.
- Adding more exercises to the dataset.
- Including fitness goals and preferences.
- Saving previous workout plans.
- Developing a graphical user interface.

## 12. Conclusion

The AI-Based Gym Workout Planner demonstrates the application of DFS and A* Search to a practical planning problem. DFS distributes muscle groups across the week, while A* selects exercises for each session. A separate validation component checks whether the generated plan follows the project's constraints.

The project demonstrates how AI search algorithms, datasets, and rule-based validation can work together in a Python application.
