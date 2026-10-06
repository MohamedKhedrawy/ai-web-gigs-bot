import os
from playwright.sync_api import sync_playwright


URL = "https://khamsat.com/community/requests"


def scrape_khamsat():
    jobs = []
    seen = set()

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
                    "Khamsat status:",
                    response.status
                )

            page.wait_for_timeout(5000)

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