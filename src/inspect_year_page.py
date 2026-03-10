import pandas as pd

# Load years list you already scraped
years = pd.read_csv("data/raw/years.csv")

# Pick a modern year (usually cleaner HTML)
row = years[years["year"] == 2024].iloc[0]
print("YEAR:", row["year"])
print("URL:", row["year_url"])