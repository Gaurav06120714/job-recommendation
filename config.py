from pathlib import Path

# Data directory and file paths
DATA_DIR = Path("data")
INDIAN_DATA = DATA_DIR / "Indian_Fresher_Salary_Skills_2025.csv"
FOREIGN_DATA = DATA_DIR / "data_cleaned_2021.csv"
MARKET_DATA = DATA_DIR / "job_market2.csv"

# Scoring weights for matching algorithm
WEIGHTS = {
    "degree": 20,
    "skills": 40,
    "location": 10,
    "salary": 10,
    "job_title": 20,
}

# Column mappings for each dataset
INDIAN_COLUMNS = {
    "role": ["role", "job_role", "job_title", "title"],
    "skills": ["skills", "primary_skills"],
    "city": ["city", "location"],
    "salary": ["salary_lpa", "salary"],
    "company": ["company"],
    "degree": ["degree"],
    "graduation_year": ["graduation_year"],
}

FOREIGN_COLUMNS = {
    "role": ["job_title", "role", "title", "position", "job title"],
    "company": ["company_name", "company", "company name"],
    "salary": ["salary_estimated", "salary", "salary estimated", "avgsalary(k)"],
    "location": ["location", "job_location", "job location"],
}

MARKET_COLUMNS = {
    "role": ["job_title", "role", "title", "job title"],
    "salary": ["monthly_salary", "salary", "monthly salary"],
}