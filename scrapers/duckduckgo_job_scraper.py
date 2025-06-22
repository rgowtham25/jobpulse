# duckduckgo_job_scraper.py

import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

# --- CONFIGURATION ---
ROLE = "Data Analyst"
LOCATION = "Bangalore"
TIME_FILTER = "qdr:h12"  # h = 1hr, h12 = 12hr, d = 1 day, w = 1 week
RESULT_LIMIT = 30        # Number of job links to fetch

# --- DUCKDUCKGO SEARCH ---
def search_duckduckgo_jobs(role, location, time_filter="qdr:h", limit=30):
    query = f"{role} jobs in {location}"
    query_encoded = urllib.parse.quote_plus(query)

    base_url = f"https://html.duckduckgo.com/html/?q={query_encoded}&t=h_&ia=web"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    job_links = []
    seen_links = set()

    results = soup.find_all("a", class_="result__a")
    for result in results:
        title = result.get_text()
        url = result["href"]

        if "uddg=" in url:
            real_url = urllib.parse.unquote(url.split("uddg=")[-1].split("&")[0])
        else:
            real_url = url

        if is_job_post(title, real_url, role) and real_url not in seen_links:
            job_links.append((title, real_url))
            seen_links.add(real_url)


        if len(job_links) >= limit:
            break
        time.sleep(0.2)  # avoid being too aggressive

    return job_links

# --- JOB FILTER ---
def is_job_post(title, url, role):
    role_keywords = role.lower().split()
    url_keywords = ["job", "jobs", "hiring", "careers", "view", "apply", "opportunity"]

    is_title_ok = all(k in title.lower() for k in role_keywords)
    is_url_ok = any(k in url.lower() for k in url_keywords) and len(url) > 60

    return is_title_ok and is_url_ok

# --- RUN ---
if __name__ == "__main__":
    print(f"\n🔍 Searching DuckDuckGo for '{ROLE} jobs in {LOCATION}' jobs posted in last {TIME_FILTER}...\n")
    job_links = search_duckduckgo_jobs(ROLE, LOCATION, time_filter=TIME_FILTER, limit=RESULT_LIMIT)

    print(f"🔍 Found {len(job_links)} job links:\n")
    for title, link in job_links:
        print(f"📌 {title}\n🔗 {link}\n")
