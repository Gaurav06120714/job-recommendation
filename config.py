from pathlib import Path

DATA_DIR = Path("data")

INDIAN_DATA = DATA_DIR / "Indian_Fresher_Salary_Skills_2025.csv"
FOREIGN_DATA = DATA_DIR / "data_cleaned_2021.csv"
MARKET_DATA = DATA_DIR / "job_market2.csv"

WEIGHTS = {
    "degree": 20,
    "skills": 40,
    "location": 10,
    "salary": 10,
    "job_title": 20,
}
