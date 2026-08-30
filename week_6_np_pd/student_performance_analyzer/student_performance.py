import numpy as np
import pandas as pd


# ============================================================
# 1. GENERATE STUDENT DATA
# ============================================================

np.random.seed(42)

NUM_STUDENTS = 100

student_ids = np.arange(1, NUM_STUDENTS + 1)

study_hours = np.round(
    np.random.uniform(1, 10, NUM_STUDENTS),
    1
)

sleep_hours = np.round(
    np.random.uniform(5, 9, NUM_STUDENTS),
    1
)

attendance = np.random.randint(
    50,
    101,
    NUM_STUDENTS
)

assignment_score = np.random.randint(
    40,
    101,
    NUM_STUDENTS
)

midterm_score = np.random.randint(
    35,
    101,
    NUM_STUDENTS
)


# ============================================================
# 2. GENERATE FINAL SCORE
# ============================================================

noise = np.random.normal(
    0,
    5,
    NUM_STUDENTS
)

final_score = (
    study_hours * 3
    + attendance * 0.15
    + assignment_score * 0.25
    + midterm_score * 0.35
    + noise
)

final_score = np.clip(
    final_score,
    0,
    100
)

final_score = np.round(
    final_score,
    1
)


# ============================================================
# 3. CREATE PANDAS DATAFRAME
# ============================================================

df = pd.DataFrame({
    "Student_ID": student_ids,
    "Study_Hours": study_hours,
    "Sleep_Hours": sleep_hours,
    "Attendance": attendance,
    "Assignment_Score": assignment_score,
    "Midterm_Score": midterm_score,
    "Final_Score": final_score
})


# ============================================================
# 4. SAVE ORIGINAL DATASET
# ============================================================

df.to_csv(
    "students.csv",
    index=False
)

print("\nOriginal dataset saved as 'students.csv'")
print("\nFirst 5 students:")
print(df.head())


# ============================================================
# 5. MAKE THE DATA DIRTY (on purpose!)
#
# Real-world data always has problems.
# We deliberately introduce them here so we can practice fixing them.
# This is called "data cleaning" and it's a CORE skill for AIML.
# ============================================================

dirty_df = df.copy()  # keep the original clean, work on a copy

# --- Problem 1: NaN (missing values) ---
# Some students didn't fill in their study hours or attendance
np.random.seed(99)
nan_idx_study  = np.random.choice(dirty_df.index, size=10, replace=False)
nan_idx_attend = np.random.choice(dirty_df.index, size=8,  replace=False)
dirty_df.loc[nan_idx_study,  "Study_Hours"] = np.nan
dirty_df.loc[nan_idx_attend, "Attendance"]  = np.nan

# --- Problem 2: Duplicate rows ---
# The first 5 students were accidentally entered twice
duplicate_rows = dirty_df.iloc[:5].copy()
dirty_df = pd.concat([dirty_df, duplicate_rows], ignore_index=True)

# --- Problem 3: Invalid values ---
# Impossible scores (must be 0-100)
dirty_df.loc[2,  "Final_Score"] = 150   # too high
dirty_df.loc[8,  "Final_Score"] = -15   # negative

# --- Problem 4: Wrong data type ---
# Assignment_Score got saved as text (string) instead of number
dirty_df["Assignment_Score"] = dirty_df["Assignment_Score"].astype(str)
dirty_df.loc[3,  "Assignment_Score"] = "N/A"
dirty_df.loc[7,  "Assignment_Score"] = "missing"
dirty_df.loc[14, "Assignment_Score"] = "eighty"

print("\n" + "=" * 60)
print("DIRTY DATA (first 10 rows)")
print("=" * 60)
print(dirty_df.head(10))
print("\nShape (rows x columns):", dirty_df.shape)


# ============================================================
# 6. DATA CLEANING — Step-by-step
# ============================================================

# We work on a copy so we don't destroy dirty_df
cleaned = dirty_df.copy()


# --- CLEANING STEP 1: Check and remove duplicates ---

print("\n" + "=" * 60)
print("STEP 1 — DUPLICATES")
print("=" * 60)

print("Number of duplicate rows:", cleaned.duplicated().sum())

cleaned = cleaned.drop_duplicates()

print("After removing duplicates, rows:", len(cleaned))


# --- CLEANING STEP 2: Fix wrong data type ---

print("\n" + "=" * 60)
print("STEP 2 — FIX DATA TYPES")
print("=" * 60)

print("Assignment_Score dtype before:", cleaned["Assignment_Score"].dtype)

# errors="coerce" means: if a value can't become a number, turn it into NaN
cleaned["Assignment_Score"] = pd.to_numeric(
    cleaned["Assignment_Score"],
    errors="coerce"
)

print("Assignment_Score dtype after: ", cleaned["Assignment_Score"].dtype)


# --- CLEANING STEP 3: Check missing values ---

print("\n" + "=" * 60)
print("STEP 3 — MISSING VALUES (NaN)")
print("=" * 60)

# isna().sum() counts how many NaN are in each column
print(cleaned.isna().sum())


# --- CLEANING STEP 4: Fill NaN with column mean ---

print("\n" + "=" * 60)
print("STEP 4 — FILL MISSING VALUES")
print("=" * 60)

# fillna() replaces NaN with a value we choose
# Using the mean is a simple and common choice
cleaned["Study_Hours"] = cleaned["Study_Hours"].fillna(
    round(cleaned["Study_Hours"].mean(), 1)
)

cleaned["Attendance"] = cleaned["Attendance"].fillna(
    round(cleaned["Attendance"].mean(), 0)
)

cleaned["Assignment_Score"] = cleaned["Assignment_Score"].fillna(
    round(cleaned["Assignment_Score"].mean(), 0)
)

print("Missing values after filling:")
print(cleaned.isna().sum())


# --- CLEANING STEP 5: Remove invalid (out-of-range) values ---

print("\n" + "=" * 60)
print("STEP 5 — REMOVE INVALID VALUES")
print("=" * 60)

invalid = cleaned[~cleaned["Final_Score"].between(0, 100)]
print("Rows with invalid Final_Score:")
print(invalid[["Student_ID", "Final_Score"]])

# Keep only rows where Final_Score is between 0 and 100
cleaned = cleaned[cleaned["Final_Score"].between(0, 100)]


# --- CLEANING STEP 6: Reset index ---

cleaned = cleaned.reset_index(drop=True)

print("\n" + "=" * 60)
print("CLEANING COMPLETE")
print("=" * 60)
print("Original dirty shape: ", dirty_df.shape)
print("Final clean shape:    ", cleaned.shape)
print("\nClean data (first 5 rows):")
print(cleaned.head())

# Use the cleaned data for all remaining analysis
df = cleaned.copy()


# ============================================================
# 7. ADD PERFORMANCE CATEGORY
# (originally section 11 — moved here since we work on clean df now)
# ============================================================

df["Performance"] = np.where(
    df["Final_Score"] >= 80,
    "Excellent",
    np.where(
        df["Final_Score"] >= 60,
        "Average",
        "Needs Improvement"
    )
)


# ============================================================
# 5. BASIC DATA INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

print("\nDataset information:")
df.info()


# ============================================================
# 6. STATISTICAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("STATISTICAL SUMMARY")
print("=" * 60)

print(
    df.describe()
)


# ============================================================
# 7. SELECTING COLUMNS
# ============================================================

print("\n" + "=" * 60)
print("COLUMN SELECTION")
print("=" * 60)

print("\nStudy hours:")
print(
    df["Study_Hours"].head()
)

print("\nStudy hours and final score:")
print(
    df[
        ["Study_Hours", "Final_Score"]
    ].head()
)


# ============================================================
# 8. FILTERING STUDENTS
# ============================================================

print("\n" + "=" * 60)
print("HIGH PERFORMERS")
print("=" * 60)

high_performers = df[
    df["Final_Score"] >= 80
]

print(high_performers)

print(
    "\nNumber of high performers:",
    len(high_performers)
)


# ============================================================
# 9. MULTIPLE CONDITIONS
# ============================================================

print("\n" + "=" * 60)
print("STRUGGLING STUDENTS")
print("=" * 60)

struggling = df[
    (df["Final_Score"] < 50)
    &
    (df["Attendance"] < 75)
]

print(struggling)

print(
    "\nNumber of struggling students:",
    len(struggling)
)


# ============================================================
# 10. STUDENTS WITH HIGH STUDY HOURS
# ============================================================

high_study = df[
    df["Study_Hours"] > 7
]

print("\n" + "=" * 60)
print("HIGH STUDY STUDENTS")
print("=" * 60)

print(high_study)


# ============================================================
# 11. PERFORMANCE CATEGORY (already added after cleaning)
# ============================================================

# Performance was added in section 7 after cleaning.
# Let's just print a preview here.

print("\n" + "=" * 60)
print("PERFORMANCE CATEGORY")
print("=" * 60)

print(
    df[
        [
            "Student_ID",
            "Final_Score",
            "Performance"
        ]
    ].head(10)
)


# ============================================================
# 12. AVERAGE VALUES
# ============================================================

print("\n" + "=" * 60)
print("AVERAGES")
print("=" * 60)

print(
    "Average Study Hours:",
    round(df["Study_Hours"].mean(), 2)
)

print(
    "Average Sleep Hours:",
    round(df["Sleep_Hours"].mean(), 2)
)

print(
    "Average Attendance:",
    round(df["Attendance"].mean(), 2)
)

print(
    "Average Assignment Score:",
    round(df["Assignment_Score"].mean(), 2)
)

print(
    "Average Midterm Score:",
    round(df["Midterm_Score"].mean(), 2)
)

print(
    "Average Final Score:",
    round(df["Final_Score"].mean(), 2)
)


# ============================================================
# 13. MEDIAN / STD / MIN / MAX
# ============================================================

print("\n" + "=" * 60)
print("FINAL SCORE STATISTICS")
print("=" * 60)

print(
    "Mean:",
    df["Final_Score"].mean()
)

print(
    "Median:",
    df["Final_Score"].median()
)

print(
    "Standard Deviation:",
    df["Final_Score"].std()
)

print(
    "Minimum:",
    df["Final_Score"].min()
)

print(
    "Maximum:",
    df["Final_Score"].max()
)


# ============================================================
# 14. TOP 5 STUDENTS
# ============================================================

print("\n" + "=" * 60)
print("TOP 5 STUDENTS")
print("=" * 60)

top_students = df.sort_values(
    by="Final_Score",
    ascending=False
).head(5)

print(
    top_students[
        [
            "Student_ID",
            "Study_Hours",
            "Attendance",
            "Final_Score"
        ]
    ]
)


# ============================================================
# 15. LOWEST 5 STUDENTS
# ============================================================

print("\n" + "=" * 60)
print("LOWEST 5 STUDENTS")
print("=" * 60)

lowest_students = df.sort_values(
    by="Final_Score"
).head(5)

print(
    lowest_students[
        [
            "Student_ID",
            "Study_Hours",
            "Attendance",
            "Final_Score"
        ]
    ]
)


# ============================================================
# 16. GROUP BY PERFORMANCE
# ============================================================

print("\n" + "=" * 60)
print("PERFORMANCE DISTRIBUTION")
print("=" * 60)

performance_count = (
    df["Performance"]
    .value_counts()
)

print(
    performance_count
)


# ============================================================
# 17. GROUPBY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("PERFORMANCE GROUP ANALYSIS")
print("=" * 60)

group_analysis = (
    df
    .groupby("Performance")
    [
        [
            "Study_Hours",
            "Attendance",
            "Final_Score"
        ]
    ]
    .mean()
)

print(
    group_analysis
)


# ============================================================
# 18. FIND STUDENT WITH HIGHEST SCORE
# ============================================================

best_student_index = (
    df["Final_Score"].idxmax()
)

best_student = df.loc[
    best_student_index
]

print("\n" + "=" * 60)
print("BEST STUDENT")
print("=" * 60)

print(best_student)


# ============================================================
# 19. FIND STUDENT WITH LOWEST SCORE
# ============================================================

worst_student_index = (
    df["Final_Score"].idxmin()
)

worst_student = df.loc[
    worst_student_index
]

print("\n" + "=" * 60)
print("LOWEST PERFORMER")
print("=" * 60)

print(worst_student)


# ============================================================
# 20. CORRELATION ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("CORRELATION ANALYSIS")
print("=" * 60)

correlation = df[
    [
        "Study_Hours",
        "Sleep_Hours",
        "Attendance",
        "Assignment_Score",
        "Midterm_Score",
        "Final_Score"
    ]
].corr()

print(
    correlation
)

print("\nStudy Hours vs Final Score:")

print(
    correlation.loc[
        "Study_Hours",
        "Final_Score"
    ]
)

print("\nAttendance vs Final Score:")

print(
    correlation.loc[
        "Attendance",
        "Final_Score"
    ]
)



# ============================================================
# 24. FINAL DATASET
# ============================================================

print("\n" + "=" * 60)
print("FINAL DATASET")
print("=" * 60)

print(
    df.head()
)


# ============================================================
# 25. SAVE FINAL DATASET
# ============================================================

df.to_csv(
    "students_analyzed.csv",
    index=False
)

print(
    "\nFinal analyzed dataset saved as "
    "'students_analyzed.csv'"
)

print("\nAnalysis completed successfully!")