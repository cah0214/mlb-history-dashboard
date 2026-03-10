import os
import sqlite3
import pandas as pd


def main():
    os.makedirs("db", exist_ok=True)

    conn = sqlite3.connect("db/mlb_history.db")

    years_df = pd.read_csv("data/raw/years.csv")
    events_df = pd.read_csv("data/raw/events.csv")

    years_df.to_sql("years", conn, if_exists="replace", index=False)
    events_df.to_sql("events", conn, if_exists="replace", index=False)

    print("Imported years and events into db/mlb_history.db")

    conn.close()


if __name__ == "__main__":
    main()