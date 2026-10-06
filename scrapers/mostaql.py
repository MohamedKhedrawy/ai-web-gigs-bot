import os
import re
from playwright.sync_api import sync_playwright


URL = "https://mostaql.com/projects?sort=latest"


def scrape_mostaql():
    jobs = []

    chromium_path = os.getenv("CHROMIUM_PATH")

    with sync_playwright() as p:

        if chromium_path:
            browser = p.chromium.launch(
                headless=True,
                executable_path=chromium_path,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )
        else:
            browser = p.chromium.launch(
                headless=True,
                channel="chrome"
            )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/130.0.0.0 Safari/537.36"
            )
        )

        try:
            response = page.goto(
                URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            if response:
                print(
                    "Mostaql status:",
                    response.status
                )

            page.wait_for_timeout(5000)

            # المشاريع بتكون في .project-row
            rows = page.locator(".project-row").all()

            for row in rows:
                try:
                    title_el = row.locator("h2 a").first

                    title = title_el.inner_text().strip()

                    if not title:
                        continue

                    link = title_el.get_attribute("href")

                    if not link:
                        continue

                    if link.startswith("/"):
                        link = "https://mostaql.com" + link

                    # الوصف
                    desc_el = row.locator(
                        ".project__brief"
                    )

                    try:
                        description = desc_el.inner_text().strip()
                    except Exception:
                        description = ""

                    jobs.append({
                        "title": title,
                        "url": link,
                        "description": description,
                        "platform": "Mostaql"
                    })

                except Exception:
                    continue

        except Exception as e:
            print(f"Mostaql page error: {e}")

        browser.close()

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