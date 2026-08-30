"""
Week 6 - Student Performance Analyzer
Streamlit Dashboard
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="🎓",
    layout="wide",
)

# ─────────────────────────────────────────────
# SIDEBAR — controls
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    seed         = st.slider("Random Seed",        0, 100, 42)
    num_students = st.slider("Number of Students", 30, 300, 100, 10)

    st.markdown("---")
    st.subheader("🔍 Filters")
    hp_threshold      = st.slider("High Performer - min score",   60, 100, 80)
    struggling_score  = st.slider("Struggling - max score",       20,  70, 50)
    struggling_attend = st.slider("Struggling - max attendance",  50,  90, 75)
    high_study_hours  = st.slider("High Study - min hours",      3.0, 9.0, 7.0, 0.5)


# ─────────────────────────────────────────────
# STEP 1 — GENERATE CLEAN DATA
# ─────────────────────────────────────────────
def generate_data(seed, num_students):
    np.random.seed(seed)

    student_ids      = np.arange(1, num_students + 1)
    study_hours      = np.round(np.random.uniform(1, 10, num_students), 1)
    sleep_hours      = np.round(np.random.uniform(5, 9,  num_students), 1)
    attendance       = np.random.randint(50, 101, num_students)
    assignment_score = np.random.randint(40, 101, num_students)
    midterm_score    = np.random.randint(35, 101, num_students)

    noise = np.random.normal(0, 5, num_students)
    final_score = (
        study_hours        * 3.0
        + attendance       * 0.15
        + assignment_score * 0.25
        + midterm_score    * 0.35
        + noise
    )
    final_score = np.clip(final_score, 0, 100)
    final_score = np.round(final_score, 1)

    df = pd.DataFrame({
        "Student_ID":       student_ids,
        "Study_Hours":      study_hours,
        "Sleep_Hours":      sleep_hours,
        "Attendance":       attendance,
        "Assignment_Score": assignment_score,
        "Midterm_Score":    midterm_score,
        "Final_Score":      final_score,
    })

    df["Performance"] = np.where(
        df["Final_Score"] >= 80, "Excellent",
        np.where(df["Final_Score"] >= 60, "Average", "Needs Improvement")
    )

    return df


# ─────────────────────────────────────────────
# STEP 2 — MAKE THE DATA DIRTY (on purpose!)
# This simulates what real-world data looks like
# ─────────────────────────────────────────────
def make_dirty_data(df):
    dirty = df.copy()

    # Problem 1: NaN (missing values) in some columns
    np.random.seed(99)
    nan_idx_study   = np.random.choice(dirty.index, size=10, replace=False)
    nan_idx_attend  = np.random.choice(dirty.index, size=8,  replace=False)
    dirty.loc[nan_idx_study,  "Study_Hours"] = np.nan
    dirty.loc[nan_idx_attend, "Attendance"]  = np.nan

    # Problem 2: Duplicate rows (same student entered twice)
    duplicate_rows = dirty.iloc[:5].copy()
    dirty = pd.concat([dirty, duplicate_rows], ignore_index=True)

    # Problem 3: Invalid / impossible values
    dirty.loc[2,  "Final_Score"] = 150   # score > 100 is impossible
    dirty.loc[8,  "Final_Score"] = -15   # negative score is impossible

    # Problem 4: Wrong data type — Assignment_Score stored as text (string)
    dirty["Assignment_Score"] = dirty["Assignment_Score"].astype(str)
    dirty.loc[3,  "Assignment_Score"] = "N/A"
    dirty.loc[7,  "Assignment_Score"] = "missing"
    dirty.loc[14, "Assignment_Score"] = "eighty"

    return dirty


# ─────────────────────────────────────────────
# STEP 3 — CLEAN THE DIRTY DATA
# Each step fixes one type of problem
# ─────────────────────────────────────────────
def clean_data(dirty_df):
    df = dirty_df.copy()

    # --- Fix 1: Remove duplicate rows ---
    rows_before = len(df)
    df = df.drop_duplicates()
    rows_after  = len(df)
    dupes_removed = rows_before - rows_after

    # --- Fix 2: Fix wrong data type (string → number) ---
    # errors="coerce" turns values that can't be converted into NaN
    df["Assignment_Score"] = pd.to_numeric(df["Assignment_Score"], errors="coerce")

    # --- Fix 3: Check NaN counts (before filling) ---
    nan_counts_before = df.isna().sum()

    # --- Fix 4: Fill NaN with the column mean ---
    df["Study_Hours"]      = df["Study_Hours"].fillna(round(df["Study_Hours"].mean(), 1))
    df["Attendance"]       = df["Attendance"].fillna(round(df["Attendance"].mean(), 0))
    df["Assignment_Score"] = df["Assignment_Score"].fillna(round(df["Assignment_Score"].mean(), 0))

    # --- Fix 5: Remove rows with invalid (out-of-range) Final Score ---
    invalid_count = len(df[~df["Final_Score"].between(0, 100)])
    df = df[df["Final_Score"].between(0, 100)]

    # --- Fix 6: Reset the index so it starts from 0 again ---
    df = df.reset_index(drop=True)

    return df, dupes_removed, nan_counts_before, invalid_count


# ─────────────────────────────────────────────
# RUN THE PIPELINE
# ─────────────────────────────────────────────
PERF_COLORS = {
    "Excellent":         "#4ade80",
    "Average":           "#fbbf24",
    "Needs Improvement": "#f87171",
}

clean_df  = generate_data(seed, num_students)
dirty_df  = make_dirty_data(clean_df)
final_df, dupes_removed, nan_counts_before, invalid_count = clean_data(dirty_df)

# Re-add Performance label on the final cleaned df
final_df["Performance"] = np.where(
    final_df["Final_Score"] >= 80, "Excellent",
    np.where(final_df["Final_Score"] >= 60, "Average", "Needs Improvement")
)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🎓 Student Performance Analyzer")
st.caption("Week 6 · NumPy & Pandas · Data Cleaning + Analysis")

st.markdown("---")

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👥 Students",        len(final_df))
c2.metric("📊 Avg Final Score", f"{final_df['Final_Score'].mean():.1f}")
c3.metric("🏆 Highest Score",   f"{final_df['Final_Score'].max():.1f}")
c4.metric("⚠️ Lowest Score",   f"{final_df['Final_Score'].min():.1f}")
c5.metric("📈 Std Deviation",   f"{final_df['Final_Score'].std():.2f}")

st.markdown("---")

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tabs = st.tabs([
    "📋 Dataset",
    "🧹 Data Cleaning",
    "📊 Statistics",
    "🔍 Filters",
    "📈 Charts",
    "🔗 Correlation",
])

# ══════════════════════════════════════════════
# TAB 1 — DATASET
# ══════════════════════════════════════════════
with tabs[0]:
    st.subheader("Dataset Overview")

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.write(f"**Shape:** {final_df.shape[0]} rows × {final_df.shape[1]} columns")
        st.dataframe(final_df.head(10), use_container_width=True)
    with col_b:
        st.write("**Column data types:**")
        dtype_df = final_df.dtypes.reset_index()
        dtype_df.columns = ["Column", "Type"]
        st.dataframe(dtype_df, use_container_width=True)

    st.subheader("Download Dataset")
    dl1, dl2 = st.columns(2)
    with dl1:
        base_cols = ["Student_ID", "Study_Hours", "Sleep_Hours", "Attendance",
                     "Assignment_Score", "Midterm_Score", "Final_Score"]
        st.download_button(
            "⬇️ Download students.csv",
            final_df[base_cols].to_csv(index=False),
            "students.csv",
            "text/csv",
        )
    with dl2:
        st.download_button(
            "⬇️ Download students_analyzed.csv",
            final_df.to_csv(index=False),
            "students_analyzed.csv",
            "text/csv",
        )

# ══════════════════════════════════════════════
# TAB 2 — DATA CLEANING
# ══════════════════════════════════════════════
with tabs[1]:
    st.subheader("🧹 Real-World Data Cleaning")
    st.write(
        "Real datasets are messy. Before doing any analysis, we need to **clean** the data. "
        "This tab shows a full cleaning pipeline — from dirty data to clean data."
    )

    # ── DIRTY DATA PREVIEW ──────────────────
    st.markdown("---")
    st.subheader("Step 0 — The Dirty (Raw) Data")
    st.write(
        f"We start with **{len(dirty_df)} rows**. "
        "The data has been deliberately made messy to simulate a real dataset."
    )
    st.dataframe(dirty_df.head(20), use_container_width=True)

    # Show what problems exist
    st.write("**Problems found in this dataset:**")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("❓ Missing Values (NaN)", int(dirty_df.isna().sum().sum()))
    col2.metric("♻️ Duplicate Rows",       int(dirty_df.duplicated().sum()))
    col3.metric("🚫 Invalid Scores",       int((~dirty_df["Final_Score"].between(0, 100)).sum()))
    col4.metric("🔤 Wrong Data Type",      "Assignment_Score = text")

    # ── STEP 1: DUPLICATES ──────────────────
    st.markdown("---")
    st.subheader("Step 1 — Remove Duplicate Rows")
    st.write(
        "Sometimes the same student gets entered into the system twice. "
        "We use `drop_duplicates()` to remove any repeated rows."
    )
    st.code(
        "# Remove rows that are completely identical\n"
        "df = df.drop_duplicates()\n\n"
        f"# Result: removed {dupes_removed} duplicate rows",
        language="python",
    )
    st.success(f"✅ Removed **{dupes_removed}** duplicate rows.")

    # ── STEP 2: WRONG DATA TYPE ─────────────
    st.markdown("---")
    st.subheader("Step 2 — Fix Wrong Data Types")
    st.write(
        "The `Assignment_Score` column was stored as **text (string)** instead of numbers. "
        "Some values like `'N/A'` or `'missing'` can't be converted — "
        "we turn those into `NaN` using `errors='coerce'`."
    )
    st.code(
        "# Convert text to numbers. Bad values become NaN.\n"
        'df["Assignment_Score"] = pd.to_numeric(df["Assignment_Score"], errors="coerce")',
        language="python",
    )
    st.info("💡 `errors='coerce'` means: if a value can't be converted, set it to NaN instead of crashing.")

    # ── STEP 3: MISSING VALUES ───────────────
    st.markdown("---")
    st.subheader("Step 3 — Handle Missing Values (NaN)")
    st.write("First, let's check how many values are missing in each column:")
    st.code("df.isna().sum()", language="python")

    nan_df = nan_counts_before.reset_index()
    nan_df.columns = ["Column", "Missing Values"]
    nan_df = nan_df[nan_df["Missing Values"] > 0]  # only show columns with NaN
    st.dataframe(nan_df, use_container_width=True)

    st.write("We fill missing values with the **mean** (average) of each column:")
    st.code(
        '# Fill missing Study_Hours with the average Study_Hours\n'
        'df["Study_Hours"] = df["Study_Hours"].fillna(df["Study_Hours"].mean())\n\n'
        '# Same for Attendance\n'
        'df["Attendance"] = df["Attendance"].fillna(df["Attendance"].mean())\n\n'
        '# Same for Assignment_Score (which now has NaN from Step 2)\n'
        'df["Assignment_Score"] = df["Assignment_Score"].fillna(df["Assignment_Score"].mean())',
        language="python",
    )
    st.success("✅ All NaN values filled with column mean.")

    # ── STEP 4: INVALID VALUES ───────────────
    st.markdown("---")
    st.subheader("Step 4 — Remove Invalid Values")
    st.write(
        "Some `Final_Score` values are impossible (e.g., `150` or `-15`). "
        "A score must be between 0 and 100. We filter those rows out."
    )
    st.code(
        "# Keep only rows where Final_Score is between 0 and 100\n"
        "df = df[df['Final_Score'].between(0, 100)]",
        language="python",
    )
    st.success(f"✅ Removed **{invalid_count}** row(s) with invalid Final Score.")

    # ── STEP 5: RESET INDEX ─────────────────
    st.markdown("---")
    st.subheader("Step 5 — Reset the Index")
    st.write(
        "After removing rows, the row numbers (index) will have gaps like 0, 1, 3, 5... "
        "We reset it so it goes 0, 1, 2, 3... cleanly."
    )
    st.code("df = df.reset_index(drop=True)", language="python")

    # ── FINAL RESULT ─────────────────────────
    st.markdown("---")
    st.subheader("✅ Final — Clean Data")
    st.write(
        f"Started with **{len(dirty_df)} rows** → "
        f"Ended with **{len(final_df)} rows** after cleaning."
    )

    b1, b2 = st.columns(2)
    with b1:
        st.write("**Dirty data (before):**")
        st.write(f"- Rows: {len(dirty_df)}")
        st.write(f"- Missing values: {int(dirty_df.isna().sum().sum())}")
        st.write(f"- Duplicates: {int(dirty_df.duplicated().sum())}")
        st.write(f"- Invalid scores: {int((~dirty_df['Final_Score'].between(0,100)).sum())}")
    with b2:
        st.write("**Clean data (after):**")
        st.write(f"- Rows: {len(final_df)}")
        st.write(f"- Missing values: {int(final_df.isna().sum().sum())}")
        st.write(f"- Duplicates: {int(final_df.duplicated().sum())}")
        st.write(f"- Invalid scores: 0")

    st.dataframe(final_df.head(10), use_container_width=True)

    # ── FULL CLEANING CODE ───────────────────
    st.markdown("---")
    st.subheader("📋 Complete Cleaning Code (all steps together)")
    st.code(
        "import pandas as pd\n\n"
        "# Step 1: Remove duplicate rows\n"
        "df = df.drop_duplicates()\n\n"
        "# Step 2: Fix wrong data type\n"
        'df["Assignment_Score"] = pd.to_numeric(df["Assignment_Score"], errors="coerce")\n\n'
        "# Step 3: Check missing values\n"
        "print(df.isna().sum())\n\n"
        "# Step 3: Fill missing values with column mean\n"
        'df["Study_Hours"]      = df["Study_Hours"].fillna(df["Study_Hours"].mean())\n'
        'df["Attendance"]       = df["Attendance"].fillna(df["Attendance"].mean())\n'
        'df["Assignment_Score"] = df["Assignment_Score"].fillna(df["Assignment_Score"].mean())\n\n'
        "# Step 4: Remove impossible values\n"
        "df = df[df['Final_Score'].between(0, 100)]\n\n"
        "# Step 5: Reset index\n"
        "df = df.reset_index(drop=True)\n\n"
        "print('Cleaning done! Shape:', df.shape)",
        language="python",
    )

# ══════════════════════════════════════════════
# TAB 3 — STATISTICS
# ══════════════════════════════════════════════
with tabs[2]:
    st.subheader("Statistical Summary")
    st.write("This shows count, mean, min, max, and more for each column.")
    num_cols = ["Study_Hours", "Sleep_Hours", "Attendance",
                "Assignment_Score", "Midterm_Score", "Final_Score"]
    st.dataframe(final_df[num_cols].describe().round(2), use_container_width=True)

    st.subheader("Performance Distribution")
    st.write("How many students fall into each category?")
    perf_counts = final_df["Performance"].value_counts().reset_index()
    perf_counts.columns = ["Performance", "Count"]
    fig_pie = px.pie(
        perf_counts,
        names="Performance",
        values="Count",
        color="Performance",
        color_discrete_map=PERF_COLORS,
        hole=0.4,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Average Values by Performance Group")
    st.write("groupby() lets us compare Excellent, Average, and Needs Improvement students.")
    group_analysis = (
        final_df.groupby("Performance")[["Study_Hours", "Attendance", "Final_Score"]]
        .mean()
        .round(2)
        .reset_index()
    )
    st.dataframe(group_analysis, use_container_width=True)

    st.subheader("🏆 Top 5 Students")
    top5 = (
        final_df.sort_values("Final_Score", ascending=False)
        .head(5)[["Student_ID", "Study_Hours", "Attendance", "Final_Score", "Performance"]]
        .reset_index(drop=True)
    )
    st.dataframe(top5, use_container_width=True)

    st.subheader("⚠️ Bottom 5 Students")
    bot5 = (
        final_df.sort_values("Final_Score")
        .head(5)[["Student_ID", "Study_Hours", "Attendance", "Final_Score", "Performance"]]
        .reset_index(drop=True)
    )
    st.dataframe(bot5, use_container_width=True)

    best  = final_df.loc[final_df["Final_Score"].idxmax()]
    worst = final_df.loc[final_df["Final_Score"].idxmin()]
    st.success(f"🥇 Best Student — ID {int(best.Student_ID)} | Score: {best.Final_Score} | Study hrs: {best.Study_Hours}")
    st.error(f"😟 Lowest Performer — ID {int(worst.Student_ID)} | Score: {worst.Final_Score} | Study hrs: {worst.Study_Hours}")

# ══════════════════════════════════════════════
# TAB 4 — FILTERS
# ══════════════════════════════════════════════
with tabs[3]:
    st.write("Use the sliders in the sidebar to change the filter values below.")

    st.subheader("High Performers")
    high_perf = final_df[final_df["Final_Score"] >= hp_threshold]
    st.write(f"Students with Final Score ≥ **{hp_threshold}**: **{len(high_perf)}** students")
    st.dataframe(high_perf.reset_index(drop=True), use_container_width=True)

    st.subheader("Struggling Students")
    struggling = final_df[
        (final_df["Final_Score"] < struggling_score) &
        (final_df["Attendance"] < struggling_attend)
    ]
    st.write(
        f"Final Score < **{struggling_score}** AND Attendance < **{struggling_attend}**: "
        f"**{len(struggling)}** students"
    )
    st.dataframe(struggling.reset_index(drop=True), use_container_width=True)

    st.subheader("High Study Students")
    high_study = final_df[final_df["Study_Hours"] > high_study_hours]
    st.write(f"Students studying > **{high_study_hours}** hrs/day: **{len(high_study)}** students")
    st.dataframe(high_study.reset_index(drop=True), use_container_width=True)

# ══════════════════════════════════════════════
# TAB 5 — CHARTS
# ══════════════════════════════════════════════
with tabs[4]:
    st.subheader("Final Score Distribution")
    st.write("A histogram shows how scores are spread out.")
    fig_hist = px.histogram(
        final_df,
        x="Final_Score",
        nbins=20,
        color="Performance",
        color_discrete_map=PERF_COLORS,
        barmode="overlay",
        opacity=0.8,
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    st.subheader("Scatter Plots")
    st.write("Do students who study more get better scores? Let's see!")
    ch1, ch2 = st.columns(2)

    with ch1:
        st.write("**Study Hours vs Final Score**")
        fig_s = px.scatter(
            final_df,
            x="Study_Hours",
            y="Final_Score",
            color="Performance",
            color_discrete_map=PERF_COLORS,
            hover_data=["Student_ID", "Attendance"],
        )
        st.plotly_chart(fig_s, use_container_width=True)

    with ch2:
        st.write("**Attendance vs Final Score**")
        fig_a = px.scatter(
            final_df,
            x="Attendance",
            y="Final_Score",
            color="Performance",
            color_discrete_map=PERF_COLORS,
            hover_data=["Student_ID", "Study_Hours"],
        )
        st.plotly_chart(fig_a, use_container_width=True)

    st.subheader("Box Plot by Performance")
    st.write("A box plot shows the range and spread of values for each group.")
    box_col = st.selectbox(
        "Pick a column to compare:",
        ["Final_Score", "Study_Hours", "Attendance", "Midterm_Score", "Assignment_Score"],
    )
    fig_box = px.box(
        final_df,
        x="Performance",
        y=box_col,
        color="Performance",
        color_discrete_map=PERF_COLORS,
        points="all",
    )
    fig_box.update_layout(showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 6 — CORRELATION
# ══════════════════════════════════════════════
with tabs[5]:
    st.subheader("Correlation with Final Score")
    st.write(
        "Correlation tells us how strongly two things are related. "
        "A value close to **1** means a strong positive link. "
        "Close to **0** means almost no link."
    )

    num_cols = ["Study_Hours", "Sleep_Hours", "Attendance",
                "Assignment_Score", "Midterm_Score", "Final_Score"]
    corr = final_df[num_cols].corr().round(3)

    key_corr = (
        corr["Final_Score"]
        .drop("Final_Score")
        .sort_values(ascending=False)
        .reset_index()
    )
    key_corr.columns = ["Feature", "Correlation with Final Score"]

    st.dataframe(key_corr, use_container_width=True)

    fig_bar = px.bar(
        key_corr,
        x="Feature",
        y="Correlation with Final Score",
        color="Correlation with Final Score",
        color_continuous_scale="RdYlGn",
        range_color=[0, 1],
        text_auto=".2f",
    )
    fig_bar.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("Week 6 · Project Bedrock · NumPy & Pandas Dashboard")
