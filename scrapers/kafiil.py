import re
from playwright.sync_api import sync_playwright

from scrapers.browser_helper import (
    create_browser,
    create_stealth_page,
    wait_for_cloudflare,
)


URL = "https://kafiil.com/projects"


def scrape_kafiil():
    jobs = []
    seen = set()

    with sync_playwright() as p:
        browser = create_browser(p)
        page = create_stealth_page(browser)

        print("Opening Kafiil...")

        response = page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        if response:
            print(
                "Kafiil status:",
                response.status
            )

        wait_for_cloudflare(page)

        links = page.locator("a").all()

        for link in links:
            try:
                href = link.get_attribute("href")

                if not href:
                    continue

                if not re.search(r"/project/\d+", href):
                    continue

                title = link.inner_text().strip()

                if not title:
                    continue

                if href.startswith("/"):
                    href = "https://kafiil.com" + href

                if href in seen:
                    continue

                # نجيب أقرب كارد يحتوي بيانات المشروع
                card = link.locator(
                    "xpath=ancestor::*[self::div or self::article][1]"
                )

                try:
                    card_text = card.inner_text().strip()
                except Exception:
                    card_text = ""

                # المشاريع المفتوحة فقط
                if "مفتوح" not in card_text:
                    continue

                seen.add(href)

                title = re.sub(
                    r"^(مفتوح|مكتمل|قيد التنفيذ)\s+",
                    "",
                    title
                ).strip()

                jobs.append({
                    "title": title,
                    "url": href,
                    "description": card_text,
                    "platform": "Kafiil"
                })

            except Exception:
                continue

        browser.close()

    print(
        "Kafiil jobs found:",
        len(jobs)
    )

    return jobs


if __name__ == "__main__":
    jobs = scrape_kafiil()

    for job in jobs[:15]:
        print("\n----------------")
        print("Title:", job["title"])
        print("URL:", job["url"])