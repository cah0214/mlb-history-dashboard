import sqlite3
import pandas as pd


def main():
    conn = sqlite3.connect("db/mlb_history.db")

    year = input("Enter a year to search: ")

    query = """
    SELECT y.year, e.category, e.event_text
    FROM years y
    JOIN events e
      ON y.year = e.year
    WHERE y.year = ?
    """

    results = pd.read_sql_query(query, conn, params=(year,))

    if results.empty:
        print("No results found.")
    else:
        print(results)

    conn.close()


if __name__ == "__main__":
    main()