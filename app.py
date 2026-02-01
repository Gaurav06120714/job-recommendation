import streamlit as st
import pandas as pd
import numpy as np
import re
import math
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Job Recommendation System", layout="wide")

# =========================================================
# DATA LOADING
# =========================================================

@st.cache_data
def load_datasets():
    df1 = pd.read_csv("data/data_cleaned_2021.csv")
    df2 = pd.read_csv("data/job_market.csv")
    df3 = pd.read_csv("data/Indian_Fresher_Salary_Skills_2025.csv")
    return df1, df2, df3


def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower()
    return df


def normalize_skills(text):
    if pd.isna(text):
        return []
    text = text.lower()
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return list(set(words))


def prepare_jobs(df1, df2):
    df1 = clean_columns(df1)
    df2 = clean_columns(df2)

    df1["skills_list"] = df1["job description"].apply(normalize_skills)
    df2["skills_list"] = df2["skills"].apply(normalize_skills)

    jobs = pd.concat([df1, df2], ignore_index=True)
    return jobs


# =========================================================
# MATCHING ENGINE
# =========================================================

def academic_score(cgpa):
    if cgpa >= 8:
        return 100
    elif cgpa >= 7:
        return 80
    else:
        return 60


def skill_score(student_skills, job_skills):
    matches = sum(skill in job_skills for skill in student_skills)
    return min(matches * 15, 100)


def final_match_score(student, job):
    a_score = academic_score(student["cgpa"])
    s_score = skill_score(student["skills"], job["skills_list"])
    score = (0.4 * s_score) + (0.2 * a_score)
    return round(score, 2)


def match_reason(student, job):
    matched = [s for s in student["skills"] if s in job["skills_list"]]
    if not matched:
        return "Few skill overlaps"
    return "Matched skills: " + ", ".join(matched)


def recommend_jobs(student, jobs_df):
    jobs_df["match_score"] = jobs_df.apply(
        lambda row: final_match_score(student, row), axis=1
    )
    return jobs_df.sort_values("match_score", ascending=False)


# =========================================================
# STUDENT PROFILE FORM
# =========================================================

def student_form():
    st.sidebar.header("Student Profile")

    name = st.sidebar.text_input("Full Name")
    degree = st.sidebar.selectbox("Degree", ["B.Tech", "B.Sc", "BCA", "MCA"])
    stream = st.sidebar.selectbox("Stream", ["CSE", "IT", "ECE", "Data Science"])
    cgpa = st.sidebar.slider("CGPA", 5.0, 10.0, 7.0)
    city = st.sidebar.text_input("City")

    skills = st.sidebar.text_area("Skills (comma separated)")

    if st.sidebar.button("Find Jobs"):
        st.session_state["student"] = {
            "name": name,
            "degree": degree,
            "stream": stream,
            "cgpa": cgpa,
            "city": city,
            "skills": [s.strip().lower() for s in skills.split(",")]
        }


# =========================================================
# VISUALIZATIONS
# =========================================================

def plot_top_skills(jobs_df):
    all_skills = []
    for s in jobs_df["skills_list"]:
        all_skills.extend(s)

    skill_counts = Counter(all_skills).most_common(10)
    skills, counts = zip(*skill_counts)

    fig, ax = plt.subplots()
    sns.barplot(x=list(counts), y=list(skills), ax=ax)
    st.pyplot(fig)


# =========================================================
# MAIN APP
# =========================================================

st.title("🎯 Smart Job Recommendation System")

df1, df2, df3 = load_datasets()
jobs_df = prepare_jobs(df1, df2)

student_form()

if "student" in st.session_state:
    student = st.session_state["student"]

    st.subheader(f"Top Matches for {student['name']}")

    results = recommend_jobs(student, jobs_df)

    # Filters
    min_score = st.slider("Minimum Match Score", 0, 100, 60)
    filtered = results[results["match_score"] >= min_score].head(20)

    for _, job in filtered.iterrows():
        title = job.get("job title", "Job")
        company = job.get("company name", "N/A")
        location = job.get("location", "N/A")

        with st.expander(f"{title} | {company} | Score: {job['match_score']}%"):
            st.write(f"**Location:** {location}")
            st.write(match_reason(student, job))

    st.subheader("📊 Most Demanded Skills")
    plot_top_skills(jobs_df)
