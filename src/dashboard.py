import sqlite3
import pandas as pd
import streamlit as st


st.set_page_config(page_title="MLB History Dashboard", layout="wide")

st.title("MLB History Dashboard ⚾")
st.caption("Crystal Hoefener | Code the Dream Web Scraping & Dashboard Project")

conn = sqlite3.connect("db/mlb_history.db")
df = pd.read_sql_query("SELECT * FROM events", conn)
conn.close()

df["year"] = pd.to_numeric(df["year"], errors="coerce")
df = df.dropna(subset=["year"])
df["year"] = df["year"].astype(int)

years = sorted(df["year"].unique())
selected_year = st.selectbox("Select a year", years, index=len(years) - 1)

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

search_text = st.text_input("Search events")

if search_text:
    filtered_df = filtered_df[
        filtered_df["event_text"].str.contains(search_text, case=False, na=False)
    ]

selected_df = filtered_df[filtered_df["year"] == selected_year]

st.subheader(f"Events for {selected_year}")
st.dataframe(selected_df, use_container_width=True)

events_per_year = filtered_df.groupby("year").size()
category_counts = filtered_df["category"].value_counts()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Events by Year")
    st.bar_chart(events_per_year)

with col2:
    st.subheader("Events by Category")
    st.bar_chart(category_counts)

st.subheader("Event Trends Over Time")
st.line_chart(events_per_year)