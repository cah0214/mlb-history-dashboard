import sqlite3
import pandas as pd
import streamlit as st


st.set_page_config(page_title="MLB History Dashboard", layout="wide")

st.title("MLB History Dashboard ⚾")
st.write("Explore historical MLB events by year and category.")

conn = sqlite3.connect("db/mlb_history.db")

df = pd.read_sql_query("SELECT * FROM events", conn)

conn.close()

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)

years = sorted(df["year"].unique())
selected_year = st.selectbox("Select a year", years, index=len(years)-1)

year_range = st.slider(
    "Select year range",
    min_value=int(df["year"].min()),
    max_value=int(df["year"].max()),
    value=(2000, int(df["year"].max()))
)

filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]

selected_df = df[df["year"] == selected_year]

st.subheader(f"Events for {selected_year}")
st.dataframe(selected_df)

st.subheader("Number of Events by Year")
events_per_year = filtered_df.groupby("year").size()
st.bar_chart(events_per_year)

st.subheader("Events by Category")
category_counts = filtered_df["category"].value_counts()
st.bar_chart(category_counts)

st.subheader("Trend of Events Over Time")
st.line_chart(events_per_year)