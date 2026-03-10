import os
import time
import pandas as pd
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def get_driver() -> webdriver.Chrome:
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--window-size=1200,900")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver


def scrape_year_links(driver: webdriver.Chrome) -> pd.DataFrame:
    anchors = driver.find_elements(By.TAG_NAME, "a")

    rows = []
    for a in anchors:
        text = (a.text or "").strip()
        href = a.get_attribute("href")

        if text.isdigit() and len(text) == 4 and href:
            year = int(text)
            if 1800 <= year <= 2100:
                rows.append({"year": year, "year_url": href})

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No year links found. The page structure may have changed.")

    df = df.drop_duplicates(subset=["year"]).sort_values("year").reset_index(drop=True)
    return df


def scrape_events_for_year(driver, year, url):
    try:
        driver.get(url)
        time.sleep(2)
    except TimeoutException:
        print(f"Timeout loading page for {year}: {url}")
        return []

    events = []
    paragraphs = driver.find_elements(By.TAG_NAME, "p")

    category = "General"

    bad_phrases = [
    "Copyright",
    "All Rights Reserved",
    "Where what happened yesterday",
    "All-Star Game |",
    "Team Standings |",
    "Hitting Statistics League Leaders",
    "Pitching Statistics League Leaders"
    ]

    for p in paragraphs:
        text = p.text.strip()

        if not text:
            continue

        if "Off the field" in text:
            category = "Off the field"
            continue
        elif "American League" in text:
            category = "American League"
            continue
        elif "National League" in text:
            category = "National League"
            continue

        if len(text) > 40:
            events.append({
                "year": year,
                "category": category,
                "event_text": text
            })

    return events


def main():

    load_dotenv()
    base_url = os.getenv("BASE_URL")

    os.makedirs("data/raw", exist_ok=True)

    driver = get_driver()

    try:

        driver.get(base_url)
        time.sleep(2)

        years_df = scrape_year_links(driver)

        print("Scraped years:", len(years_df))

        years_df.to_csv("data/raw/years.csv", index=False)

        # NEW LOOP
        all_events = []

        for _, row in years_df.iterrows():

            year = int(row["year"])
            url = row["year_url"]

            print(f"Scraping events for {year}")

            events = scrape_events_for_year(driver, year, url)

            print(f"Found {len(events)} events")

            all_events.extend(events)

        events_df = pd.DataFrame(all_events)

        events_df.to_csv("data/raw/events.csv", index=False)

        print("Saved to data/raw/events.csv")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()