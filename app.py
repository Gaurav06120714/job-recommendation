import streamlit as st
import pandas as pd
from config import DATA_PATH, JOB_PATH, SALARY_PATH

st.set_page_config(page_title="Job Recommendation System")

st.title("🎯 Job Recommendation for Students")

@st.cache_data
def load_data():
    df1 = pd.read_csv(DATA_PATH)
    df2 = pd.read_csv(JOB_PATH)
    df3 = pd.read_csv(SALARY_PATH)
    return df1, df2, df3

students, jobs, salary = load_data()

st.sidebar.header("Enter Your Details")

name = st.sidebar.text_input("Your Name")
skills = st.sidebar.text_area("Enter your skills (comma separated)")
cgpa = st.sidebar.slider("CGPA", 5.0, 10.0, 7.0)

if st.sidebar.button("Recommend Jobs"):

    st.subheader(f"Hi {name}, Recommended Jobs for You")

    skill_list = [s.strip().lower() for s in skills.split(",")]

    jobs['score'] = jobs['skills'].apply(
        lambda x: sum(skill in x.lower() for skill in skill_list)
    )

    recommended = jobs.sort_values(by='score', ascending=False).head(5)

    st.dataframe(recommended[['job_title', 'company', 'skills']])

    st.subheader("💰 Expected Salary")
    st.dataframe(salary.head(5))