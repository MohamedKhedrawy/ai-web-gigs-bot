from playwright.sync_api import sync_playwright

from scrapers.browser_helper import (
    create_browser,
    create_stealth_page,
    wait_for_cloudflare,
)


URL = "https://nafezly.com/projects"


def scrape_nafezly():
    jobs = []
    seen = set()

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
                    "Nafezly status:",
                    response.status
                )

            wait_for_cloudflare(page)

            links = page.locator("a").all()

            for link in links:
                try:
                    href = link.get_attribute("href")

                    if not href:
                        continue

                    # روابط المشاريع فقط
                    if "/project/" not in href:
                        continue

                    title = link.inner_text().strip()

                    if not title:
                        continue

                    if href.startswith("/"):
                        href = "https://nafezly.com" + href

                    if href in seen:
                        continue

                    seen.add(href)

                    jobs.append({
                        "title": title,
                        "url": href,
                        "description": "",
                        "platform": "Nafezly"
                    })

                except Exception:
                    continue

        except Exception as e:
            print(f"Nafezly page error: {e}")

        browser.close()

    print(
        "Nafezly jobs found:",
        len(jobs)
    )

    return jobs


if __name__ == "__main__":
    jobs = scrape_nafezly()

    for job in jobs[:10]:
        print("\n----------------")
        print("Title:", job["title"])
        print("URL:", job["url"])