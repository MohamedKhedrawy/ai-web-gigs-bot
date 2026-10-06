from curl_cffi import requests as cffi_requests
from bs4 import BeautifulSoup


URL = "https://mostaql.com/projects?sort=latest"

HEADERS = {
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
    "Referer": "https://mostaql.com/",
}


def scrape_mostaql():
    response = cffi_requests.get(
        URL,
        headers=HEADERS,
        impersonate="chrome",
        timeout=20
    )

    print("Mostaql status:", response.status_code)

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    projects = soup.select(".project-row")

    jobs = []

    for project in projects:

        title_element = project.select_one("h2 a")

        if not title_element:
            continue

        title = title_element.get_text(
            " ",
            strip=True
        )

        link = title_element.get("href")

        if not link:
            continue

        if link.startswith("/"):
            link = "https://mostaql.com" + link

        description_element = project.select_one(
            ".project__brief"
        )

        description = (
            description_element.get_text(
                " ",
                strip=True
            )
            if description_element
            else ""
        )

        jobs.append({
            "title": title,
            "url": link,
            "description": description,
            "platform": "Mostaql"
        })

    print(
        "Mostaql jobs found:",
        len(jobs)
    )

    return jobs


if __name__ == "__main__":
    jobs = scrape_mostaql()

    for job in jobs[:10]:
        print("\n----------------")
        print("Title:", job["title"])
        print("URL:", job["url"])