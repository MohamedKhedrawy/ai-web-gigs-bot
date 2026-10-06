import os
from curl_cffi import requests as cffi_requests
from bs4 import BeautifulSoup


URL = "https://nafezly.com/projects"

HEADERS = {
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
    "Referer": "https://nafezly.com/",
}


def scrape_nafezly():
    proxy_url = os.getenv("PROXY_URL")

    proxies = None
    if proxy_url:
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }

    response = cffi_requests.get(
        URL,
        headers=HEADERS,
        impersonate="chrome",
        proxies=proxies,
        timeout=30
    )

    print("Nafezly status:", response.status_code)

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

    print(
        "Nafezly jobs found:",
        len(unique)
    )

    return list(unique.values())


if __name__ == "__main__":
    jobs = scrape_nafezly()

    for job in jobs[:10]:
        print("\n----------------")
        print("Title:", job["title"])
        print("URL:", job["url"])