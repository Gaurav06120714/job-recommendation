import streamlit as st
import pandas as pd
import numpy as np
from config import *

def standardize_columns(df):
    """Standardize column names to lowercase with underscores"""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )
    return df

def find_col(df, options):
    """Find the first matching column from a list of options"""
    for c in options:
        if c in df.columns:
            return c
    return None

def safe_get_value(row, col, default=""):
    """Safely get a value from a row, returning default if not found"""
    if col is None or col not in row.index:
        return default
    value = row.get(col, default)
    return value if pd.notna(value) else default

# Page configuration
st.set_page_config(layout="wide", page_title="AI Job Recommendation System", page_icon="🎯")

# Custom CSS
st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
.big-title {font-size:60px; font-weight:bold; text-align:center; color:#4CAF50;}
.center {text-align:center; font-size:18px; margin-bottom:30px;}
.card {
    background: linear-gradient(135deg, #1c1f26 0%, #2a2d35 100%);
    padding:25px;
    border-radius:15px;
    margin:15px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    border-left: 4px solid #4CAF50;
}
.score-card {
    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    padding:30px;
    border-radius:15px;
    text-align:center;
    margin:20px 0;
    box-shadow: 0 6px 12px rgba(76,175,80,0.3);
}
.score-number {
    font-size:72px;
    font-weight:bold;
    color:white;
    margin:10px 0;
}
.card h3 {color:#4CAF50; margin-bottom:15px;}
.stButton>button {
    background-color:#4CAF50;
    color:white;
    font-size:18px;
    padding:12px 30px;
    border-radius:8px;
    border:none;
    font-weight:bold;
}
.stButton>button:hover {
    background-color:#45a049;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and standardize all datasets"""
    try:
        indian = standardize_columns(pd.read_csv(INDIAN_DATA))
        foreign = standardize_columns(pd.read_csv(FOREIGN_DATA))
        market = standardize_columns(pd.read_csv(MARKET_DATA))
        return indian, foreign, market
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None

# Load data
indian_df, foreign_df, market_df = load_data()

if indian_df is None or foreign_df is None or market_df is None:
    st.error("Failed to load data files. Please check if CSV files exist in the 'data' folder.")
    st.stop()

# Navigation
page = st.sidebar.radio("Navigation", ["🏠 Home", "🎓 Student Profile", "📊 Data Info"])

if page == "🏠 Home":
    st.markdown('<div class="big-title">🎯 AI Job Recommendation System</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div class='center'>Match your profile with the best companies using intelligent scoring.<br>"
        "Get recommendations from Indian companies, foreign opportunities, and market salary insights.</div>",
        unsafe_allow_html=True
    )
   
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card">
        <h3>🇮🇳 Indian Companies</h3>
        <p>Get matched with top Indian companies based on your skills, location, and preferences.</p>
        </div>
        """, unsafe_allow_html=True)
   
    with col2:
        st.markdown("""
        <div class="card">
        <h3>🌍 Foreign Opportunities</h3>
        <p>Explore international job opportunities that match your profile.</p>
        </div>
        """, unsafe_allow_html=True)
   
    with col3:
        st.markdown("""
        <div class="card">
        <h3>💰 Market Insights</h3>
        <p>Understand expected salary ranges for your desired role.</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "📊 Data Info":
    st.title("📊 Dataset Information")
   
    st.markdown(f"""
    <div class="card">
    <h3>Loaded Datasets</h3>
    <p><strong>Indian Companies:</strong> {len(indian_df)} records</p>
    <p><strong>Foreign Companies:</strong> {len(foreign_df)} records</p>
    <p><strong>Market Data:</strong> {len(market_df)} records</p>
    </div>
    """, unsafe_allow_html=True)
   
    with st.expander("View Indian Dataset Sample"):
        st.dataframe(indian_df.head())
   
    with st.expander("View Foreign Dataset Sample"):
        st.dataframe(foreign_df.head())
   
    with st.expander("View Market Dataset Sample"):
        st.dataframe(market_df.head())

elif page == "🎓 Student Profile":
    st.title("🎓 Student Information Form")
    st.markdown("Fill in your details to get personalized job recommendations")
   
    col1, col2 = st.columns(2)
   
    with col1:
        name = st.text_input("Full Name", placeholder="Enter your full name")
        college = st.text_input("College Name", placeholder="Enter your college name")
        degree = st.selectbox("Degree", ["B.Tech", "B.Sc", "BCA", "M.Tech", "MCA", "M.Sc"])
        grad_year = st.number_input("Graduation Year", 2020, 2030, 2025)
        marks = st.slider("Total Percentage", 0, 100, 75)
   
    with col2:
        location = st.text_input("Preferred Location", placeholder="e.g., Bangalore, Mumbai")
        job_title = st.text_input("Preferred Job Role", placeholder="e.g., Software Engineer, Data Analyst")
        skills = st.text_area("Your Skills (comma separated)", placeholder="e.g., Python, Java, SQL, Machine Learning")
        expected_salary = st.number_input("Expected Salary (LPA)", 0.0, 100.0, 5.0, 0.5)
   
    st.markdown("---")
   
    if st.button("🔍 Find My Jobs", use_container_width=True):
        if not name or not job_title or not skills:
            st.warning("⚠️ Please fill in at least Name, Job Role, and Skills to get recommendations.")
        else:
            with st.spinner("Analyzing your profile and matching with opportunities..."):
                # Process skills
                skill_list = [s.strip().lower() for s in skills.split(",") if s.strip()]
               
                # Find column names for Indian dataset
                ind_role = find_col(indian_df, INDIAN_COLUMNS["role"])
                ind_skills = find_col(indian_df, INDIAN_COLUMNS["skills"])
                ind_city = find_col(indian_df, INDIAN_COLUMNS["city"])
                ind_salary = find_col(indian_df, INDIAN_COLUMNS["salary"])
                ind_company = find_col(indian_df, INDIAN_COLUMNS["company"])
                ind_degree = find_col(indian_df, INDIAN_COLUMNS["degree"])
               
                # Find column names for Foreign dataset
                for_role = find_col(foreign_df, FOREIGN_COLUMNS["role"])
                for_company = find_col(foreign_df, FOREIGN_COLUMNS["company"])
                for_salary = find_col(foreign_df, FOREIGN_COLUMNS["salary"])
                for_location = find_col(foreign_df, FOREIGN_COLUMNS["location"])
               
                # Find column names for Market dataset
                mar_role = find_col(market_df, MARKET_COLUMNS["role"])
                mar_salary = find_col(market_df, MARKET_COLUMNS["salary"])
               
                # Calculate score for Indian companies
                def calculate_indian_score(row):
                    score = 0
                   
                    # Degree match
                    if ind_degree and degree.lower() in str(safe_get_value(row, ind_degree, "")).lower():
                        score += WEIGHTS["degree"]
                   
                    # Job title match
                    if ind_role and job_title.lower() in str(safe_get_value(row, ind_role, "")).lower():
                        score += WEIGHTS["job_title"]
                   
                    # Skills match
                    if ind_skills:
                        job_skills = str(safe_get_value(row, ind_skills, "")).lower()
                        match_count = sum(1 for s in skill_list if s in job_skills)
                        if len(skill_list) > 0:
                            score += (match_count / len(skill_list)) * WEIGHTS["skills"]
                   
                    # Location match
                    if ind_city and location and location.lower() in str(safe_get_value(row, ind_city, "")).lower():
                        score += WEIGHTS["location"]
                   
                    # Salary match
                    if ind_salary:
                        try:
                            job_salary = float(safe_get_value(row, ind_salary, 0) or 0)
                            if expected_salary <= job_salary:
                                score += WEIGHTS["salary"]
                        except:
                            pass
                   
                    return score
               
                # Score Indian companies
                indian_df["score"] = indian_df.apply(calculate_indian_score, axis=1)
                top_indian = indian_df.sort_values("score", ascending=False).head(5)
                best_indian = top_indian.iloc[0] if len(top_indian) > 0 else None
               
                # Find best foreign match
                best_foreign = None
                if for_role:
                    foreign_df["match_score"] = 0
                   
                    # Role match
                    foreign_df["role_match"] = (
                        foreign_df[for_role]
                        .astype(str)
                        .str.lower()
                        .str.contains(job_title.lower(), na=False)
                    )
                    foreign_df.loc[foreign_df["role_match"], "match_score"] += 50
                   
                    # Skills match
                    for skill in skill_list:
                        skill_cols = [col for col in foreign_df.columns if skill in col.lower()]
                        for col in skill_cols:
                            foreign_df.loc[foreign_df[col] == 1, "match_score"] += 10
                   
                    # Location match
                    if for_location and location:
                        foreign_df.loc[
                            foreign_df[for_location].astype(str).str.lower().str.contains(location.lower(), na=False),
                            "match_score"
                        ] += 20
                   
                    matched_foreign = foreign_df[foreign_df["match_score"] > 0].sort_values("match_score", ascending=False)
                    best_foreign = matched_foreign.iloc[0] if len(matched_foreign) > 0 else None
               
                # Find best market salary
                best_market = None
                if mar_role:
                    market_df["match"] = (
                        market_df[mar_role]
                        .astype(str)
                        .str.lower()
                        .str.contains(job_title.lower(), na=False)
                    )
                    matched_market = market_df[market_df["match"]]
                    best_market = matched_market.iloc[0] if len(matched_market) > 0 else None
               
                # Display results
                st.markdown("---")
                st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🎯 Your Personalized Recommendations</h1>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
               
                # Student summary
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"""
                    <div class="card">
                    <h3>👤 Student Summary</h3>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>College:</strong> {college}</p>
                    <p><strong>Degree:</strong> {degree}</p>
                    <p><strong>Marks:</strong> {marks}%</p>
                    <p><strong>Graduation:</strong> {grad_year}</p>
                    <p><strong>Preferred Location:</strong> {location}</p>
                    <p><strong>Preferred Role:</strong> {job_title}</p>
                    <p><strong>Expected Salary:</strong> ₹{expected_salary} LPA</p>
                    </div>
                    """, unsafe_allow_html=True)
               
                with col2:
                    if best_indian is not None:
                        st.markdown(f"""
                        <div class="score-card">
                        <h3 style="color:white; margin:0;">Match Score</h3>
                        <div class="score-number">{int(best_indian['score'])}</div>
                        <p style="color:white; font-size:20px; margin:0;">out of 100</p>
                        </div>
                        """, unsafe_allow_html=True)
               
                # Best Indian Company
                if best_indian is not None:
                    st.markdown(f"""
                    <div class="card">
                    <h3>🇮🇳 Best Indian Company Match</h3>
                    <p><strong>Company:</strong> {safe_get_value(best_indian, ind_company, "N/A")}</p>
                    <p><strong>Role:</strong> {safe_get_value(best_indian, ind_role, "N/A")}</p>
                    <p><strong>Location:</strong> {safe_get_value(best_indian, ind_city, "N/A")}</p>
                    <p><strong>Salary:</strong> ₹{safe_get_value(best_indian, ind_salary, "N/A")} LPA</p>
                    <p><strong>Skills Required:</strong> {safe_get_value(best_indian, ind_skills, "N/A")}</p>
                    <p><strong>Match Score:</strong> {int(best_indian['score'])}/100</p>
                    </div>
                    """, unsafe_allow_html=True)
                   
                    # Show top 5 matches
                    if len(top_indian) > 1:
                        with st.expander("📋 View More Indian Company Matches"):
                            for idx, row in top_indian.iloc[1:].iterrows():
                                st.markdown(f"""
                                **{safe_get_value(row, ind_company, "N/A")}** - {safe_get_value(row, ind_role, "N/A")}  
                                Salary: ₹{safe_get_value(row, ind_salary, "N/A")} LPA | Score: {int(row['score'])}/100
                                """)
                else:
                    st.warning("No matching Indian companies found.")
               
                # Best Foreign Company
                col1, col2 = st.columns(2)
               
                with col1:
                    if best_foreign is not None:
                        st.markdown(f"""
                        <div class="card">
                        <h3>🌍 Best Foreign Company Match</h3>
                        <p><strong>Company:</strong> {safe_get_value(best_foreign, for_company, "N/A")}</p>
                        <p><strong>Role:</strong> {safe_get_value(best_foreign, for_role, "N/A")}</p>
                        <p><strong>Location:</strong> {safe_get_value(best_foreign, for_location, "N/A")}</p>
                        <p><strong>Estimated Salary:</strong> {safe_get_value(best_foreign, for_salary, "N/A")}</p>
                        <p><strong>Match Score:</strong> {int(best_foreign['match_score'])}/100</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("🌍 No matching foreign companies found for your profile.")
               
                with col2:
                    if best_market is not None:
                        st.markdown(f"""
                        <div class="card">
                        <h3>💰 Expected Market Salary</h3>
                        <p><strong>Role:</strong> {safe_get_value(best_market, mar_role, "N/A")}</p>
                        <p><strong>Monthly Salary:</strong> ₹{safe_get_value(best_market, mar_salary, "N/A")}</p>
                        <p><strong>Annual Estimate:</strong> ₹{float(safe_get_value(best_market, mar_salary, 0) or 0) * 12:,.0f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("💰 No market salary data found for your preferred role.")
               
                # Skills analysis
                if best_indian is not None and ind_skills:
                    st.markdown("---")
                    st.markdown("<h3 style='color:#4CAF50;'>📊 Skills Analysis</h3>", unsafe_allow_html=True)
                   
                    job_skills = str(safe_get_value(best_indian, ind_skills, "")).lower().split(",")
                    job_skills = [s.strip() for s in job_skills if s.strip()]
                   
                    matched_skills = [s for s in skill_list if any(s in js for js in job_skills)]
                    missing_skills = [js for js in job_skills[:5] if not any(s in js for s in skill_list)]
                   
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success(f"✅ **Matched Skills ({len(matched_skills)}):**")
                        st.write(", ".join(matched_skills) if matched_skills else "None")
                   
                    with col2:
                        if missing_skills:
                            st.warning(f"📚 **Skills to Learn ({len(missing_skills)}):**")
                            st.write(", ".join(missing_skills[:5]))
               
                st.balloons()
