import requests
from bs4 import BeautifulSoup


URL = "https://nafezly.com/projects"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://nafezly.com/",
    "Connection": "keep-alive",
}


def scrape_nafezly():
    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    jobs = []

    # هنبدأ بالسحب العام للروابط
    for link in soup.find_all("a", href=True):

        href = link.get("href", "")
        title = link.get_text(
            " ",
            strip=True
        )

        if not title:
            continue

        # روابط المشاريع فقط
        if "/project/" not in href:
            continue

        if href.startswith("/"):
            href = "https://nafezly.com" + href

        jobs.append({
            "title": title,
            "url": href,
            "description": "",
            "platform": "Nafezly"
        })

    # إزالة التكرار
    unique = {}

    for job in jobs:
        unique[job["url"]] = job

    return list(unique.values())