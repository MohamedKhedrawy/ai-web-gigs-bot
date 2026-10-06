from playwright.sync_api import sync_playwright

from scrapers.browser_helper import (
    create_browser,
    create_stealth_page,
    wait_for_cloudflare,
)


URL = "https://mostaql.com/projects?sort=latest"


def scrape_mostaql():
    jobs = []

    with sync_playwright() as p:
        browser = create_browser(p)
        page = create_stealth_page(browser)

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

            wait_for_cloudflare(page)

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