from curl_cffi import requests as cffi_requests
from bs4 import BeautifulSoup


URL = "https://khamsat.com/community/requests"

HEADERS = {
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
    "Referer": "https://khamsat.com/",
}


def scrape_khamsat():
    response = cffi_requests.get(
        URL,
        headers=HEADERS,
        impersonate="chrome",
        timeout=20
    )

    print("Khamsat status:", response.status_code)

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    jobs = []

    for link in soup.find_all("a", href=True):

        href = link.get("href", "")
        title = link.get_text(
            " ",
            strip=True
        )

        if not title:
            continue

        # لازم يكون رابط طلب
        if "/community/requests/" not in href:
            continue

        # استبعاد إنشاء موضوع جديد
        if href.endswith("/new"):
            continue

        if title == "موضوع جديد":
            continue

        if href.startswith("/"):
            href = "https://khamsat.com" + href

        jobs.append({
            "title": title,
            "url": href,
            "description": "",
            "platform": "Khamsat"
        })

    # Remove duplicates
    unique = {}

    for job in jobs:
        unique[job["url"]] = job

    print(
        "Khamsat jobs found:",
        len(unique)
    )

    return list(unique.values())


if __name__ == "__main__":
    jobs = scrape_khamsat()

    for job in jobs[:10]:
        print("\n----------------")
        print(job["title"])
        print(job["url"])