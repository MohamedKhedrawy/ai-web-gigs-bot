import requests
from bs4 import BeautifulSoup


URL = "https://mostaql.com/projects?sort=latest"

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
    "Referer": "https://mostaql.com/",
    "Connection": "keep-alive",
}


def scrape_mostaql():
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

    return jobs