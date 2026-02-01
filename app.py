import streamlit as st
import pandas as pd
import numpy as np
from config import *
st.set_page_config(layout="wide")

st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
.big-title {font-size:60px; font-weight:bold; text-align:center;}
.center {text-align:center;}
.card {
    background-color:#1c1f26;
    padding:20px;
    border-radius:10px;
    margin:10px 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    indian = pd.read_csv(INDIAN_DATA)
    foreign = pd.read_csv(FOREIGN_DATA)
    market = pd.read_csv(MARKET_DATA)
    return indian, foreign, market

indian_df, foreign_df, market_df = load_data()

page = st.sidebar.radio("Navigation", ["🏠 Home", "🎓 Student Profile"])

if page == "🏠 Home":
    st.markdown('<div class="big-title">AI Job Recommendation System</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div class='center'>This system matches your profile with the best companies using intelligent scoring.</div>",
        unsafe_allow_html=True
    )

elif page == "🎓 Student Profile":

    st.title("Student Information Form")

    name = st.text_input("Full Name")
    college = st.text_input("College Name")
    degree = st.selectbox("Degree", ["B.Tech", "B.Sc", "BCA", "M.Tech"])
    grad_year = st.number_input("Graduation Year", 2020, 2030)
    marks = st.slider("Total Percentage", 0, 100)
    location = st.text_input("Preferred Location")
    job_title = st.text_input("Preferred Job Role")
    skills = st.text_area("Your Skills (comma separated)")
    expected_salary = st.number_input("Expected Salary LPA")

    if st.button("Find My Jobs"):

        skill_list = [s.strip().lower() for s in skills.split(",")]

        def calculate_score(row):
            score = 0

            if degree.lower() in str(row.get("Degree", "")).lower():
                score += WEIGHTS["degree"]

            if job_title.lower() in str(row.get("Role", "")).lower():
                score += WEIGHTS["job_title"]

            job_skills = str(row.get("Skills", "")).lower()
            match_count = sum(1 for s in skill_list if s in job_skills)
            skill_score = (match_count / max(len(skill_list),1)) * WEIGHTS["skills"]
            score += skill_score

            if location.lower() in str(row.get("City", "")).lower():
                score += WEIGHTS["location"]

            if expected_salary <= row.get("Salary_lpa", 0):
                score += WEIGHTS["salary"]

            return score

        indian_df["Score"] = indian_df.apply(calculate_score, axis=1)
        best_indian = indian_df.sort_values("Score", ascending=False).iloc[0]

        foreign_df["match"] = foreign_df["Job title"].str.lower().str.contains(job_title.lower(), na=False)
        best_foreign = foreign_df[foreign_df["match"]].iloc[0] if not foreign_df[foreign_df["match"]].empty else None

        market_df["match"] = market_df["job title"].str.lower().str.contains(job_title.lower(), na=False)
        best_market = market_df[market_df["match"]].iloc[0] if not market_df[market_df["match"]].empty else None

        st.markdown("---")
        st.header("🎯 Recommendation Result")

        st.markdown(f"""
        <div class="card">
        <h3>Student Summary</h3>
        Name: {name} <br>
        College: {college} <br>
        Marks: {marks}% <br>
        Graduation: {grad_year}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
        <h3>Match Score</h3>
        <h1>{int(best_indian['Score'])} / 100</h1>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
        <h3>🇮🇳 Best Indian Company</h3>
        Company: {best_indian['Company']} <br>
        Role: {best_indian['Role']} <br>
        Salary: {best_indian['Salary_lpa']} LPA
        </div>
        """, unsafe_allow_html=True)

        if best_foreign is not None:
            st.markdown(f"""
            <div class="card">
            <h3>🌍 Best Foreign Company</h3>
            Company: {best_foreign['Company name']} <br>
            Role: {best_foreign['Job title']} <br>
            Salary: {best_foreign['Salary estimated']}
            </div>
            """, unsafe_allow_html=True)

        if best_market is not None:
            st.markdown(f"""
            <div class="card">
            <h3>💰 Expected Market Salary</h3>
            Role: {best_market['job title']} <br>
            Monthly Salary: {best_market['Monthly salary']}
            </div>
            """, unsafe_allow_html=True)
