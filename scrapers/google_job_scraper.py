# from serpapi import GoogleSearch

# def fetch_real_job_posts(role="Data Analyst", location="Bangalore"):
#     query = f"{role} jobs in {location}"
#     params = {
#         "engine": "google",
#         "q": query,
#         "hl": "en",
#         "tbs": "qdr:h12",  # Past 1 hour
#         "api_key": "9902faf3ebf3a49dde714da3908ca1ab9df46189cfae448aeb4b3d3c6a7bc165"
#     }

#     search = GoogleSearch(params)
#     results = search.get_dict()

#     INDIVIDUAL_JOB_PATTERNS = [
#         "linkedin.com/jobs/view/",
#         "naukri.com/job-listings",
#         "indeed.com/viewjob",
#         "tcs.com/careers/job",
#         "glassdoor.co.in/Job/",
#         "zoho.com/jobs/Careers",
#         "freshersworld.com/job/",
#         "monstergulf.com/job",
#         "hirect.in/job/"
#     ]

#     job_links = []
#     for result in results.get("organic_results", []):
#         title = result.get("title", "")
#         link = result.get("link", "")
#         if any(pattern in link for pattern in INDIVIDUAL_JOB_PATTERNS):
#             job_links.append((title, link))

#     return job_links


# if __name__ == "__main__":
#     role = "Data Analyst"
#     location = "Bangalore"
#     job_links = fetch_real_job_posts(role, location)

#     print(f"\n🔍 Found {len(job_links)} real job post links (posted in last 1 hour):\n")
#     for title, link in job_links:
#         print(f"📌 {title}\n🔗 {link}\n")

#########################---------------------------------------------------------------------------------------------

# google_job_scraper.py
# from serpapi import GoogleSearch
from serpapi.google_search_results import GoogleSearchResults as GoogleSearch


# --- CONFIGURATION ---
ROLE = "Data Analyst"
LOCATION = "Bangalore"
TIME_FILTER = "h"  # Options: h (1hr), h12 (12hr), d (1 day), w (1 week)
MAX_PAGES = 3
SERPAPI_KEY = "9902faf3ebf3a49dde714da3908ca1ab9df46189cfae448aeb4b3d3c6a7bc165"  # Replace with your actual key

# --- FILTERING RULES ---
def is_job_title(text: str) -> bool:
    keywords = ["hiring", "analyst", "developer", "engineer", "career", "vacancy", "job"]
    text_lower = text.lower()
    return any(k in text_lower for k in keywords) or "data analyst" in text_lower


def is_job_url(url: str) -> bool:
    valid_keywords = ["job", "jobs", "hiring", "careers", "vacancy", "apply"]
    return any(k in url.lower() for k in valid_keywords) and url.startswith("http") and len(url) > 40


def is_valid_job(title: str, url: str) -> bool:
    return is_job_title(title) and is_job_url(url)

# --- FETCH FUNCTION ---
def fetch_job_links(role, location, time_filter="h", max_pages=3):
    job_links = []
    query = f"{role} jobs in {location}"

    for start in range(0, max_pages * 30, 30):
        print(f"🌐 Fetching results from start={start}...")
        params = {
            "engine": "google",
            "q": query,
            "hl": "en",
            "tbs": f"qdr:{time_filter}",
            "num": 30,
            "start": start,
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        for result in results.get("organic_results", []):
            title = result.get("title", "")
            link = result.get("link", "")
            print(f"👀 Checking: {title} | {link}")
            if is_valid_job(title, link) and (title, link) not in job_links:
                job_links.append((title, link))


    return job_links

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    job_links = fetch_job_links(ROLE, LOCATION, TIME_FILTER, MAX_PAGES)
    print(f"\n🔍 Found {len(job_links)} valid job post links (posted in last {TIME_FILTER}):\n")
    for title, link in job_links:
        print(f"📌 {title}\n🔗 {link}\n")
