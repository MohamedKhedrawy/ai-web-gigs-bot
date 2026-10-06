from playwright.sync_api import sync_playwright

from scrapers.browser_helper import (
    create_browser,
    create_stealth_page,
    wait_for_cloudflare,
)


URL = "https://khamsat.com/community/requests"


def scrape_khamsat():
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
                    "Khamsat status:",
                    response.status
                )

            wait_for_cloudflare(page)

            links = page.locator("a").all()

            for link in links:
                try:
                    href = link.get_attribute("href")

                    if not href:
                        continue

                    # لازم يكون رابط طلب
                    if "/community/requests/" not in href:
                        continue

                    # استبعاد إنشاء موضوع جديد
                    if href.endswith("/new"):
                        continue

                    title = link.inner_text().strip()

                    if not title:
                        continue

                    if title == "موضوع جديد":
                        continue

                    if href.startswith("/"):
                        href = "https://khamsat.com" + href

                    if href in seen:
                        continue

                    seen.add(href)

                    jobs.append({
                        "title": title,
                        "url": href,
                        "description": "",
                        "platform": "Khamsat"
                    })

                except Exception:
                    continue

        except Exception as e:
            print(f"Khamsat page error: {e}")

        browser.close()

    print(
        "Khamsat jobs found:",
        len(jobs)
    )

    return jobs


if __name__ == "__main__":
    jobs = scrape_khamsat()

    print(
        "Khamsat jobs found:",
        len(jobs)
    )

    for job in jobs[:10]:
        print("\n----------------")
        print(job["title"])
        print(job["url"])