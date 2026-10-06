import os


# أرجمنتات إضافية لتفادي كشف البوت
STEALTH_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features=AutomationControlled",
    "--disable-features=IsolateOrigins,site-per-process",
    "--disable-infobars",
    "--window-size=1920,1080",
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/130.0.0.0 Safari/537.36"
)

# سكريبت جافاسكريبت لإخفاء إشارات الأتمتة
STEALTH_JS = """
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});

Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
});

Object.defineProperty(navigator, 'languages', {
    get: () => ['ar', 'en-US', 'en']
});

window.chrome = { runtime: {} };

const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications'
        ? Promise.resolve({ state: Notification.permission })
        : originalQuery(parameters)
);
"""


def create_browser(playwright):
    """إنشاء متصفح مع إعدادات التخفي"""

    chromium_path = os.getenv("CHROMIUM_PATH")

    if chromium_path:
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=chromium_path,
            args=STEALTH_ARGS
        )
    else:
        browser = playwright.chromium.launch(
            headless=True,
            channel="chrome",
            args=STEALTH_ARGS
        )

    return browser


def create_stealth_page(browser):
    """إنشاء صفحة مع إعدادات التخفي"""

    context = browser.new_context(
        user_agent=USER_AGENT,
        viewport={"width": 1920, "height": 1080},
        locale="ar-EG",
        timezone_id="Africa/Cairo",
    )

    context.add_init_script(STEALTH_JS)

    page = context.new_page()

    return page


def wait_for_cloudflare(page, timeout=15000):
    """انتظار تجاوز تحدي Cloudflare"""

    try:
        # انتظار اختفاء صفحة التحقق
        page.wait_for_function(
            """
            () => {
                const title = document.title.toLowerCase();
                const body = document.body
                    ? document.body.innerText
                    : '';

                // لسه في صفحة Cloudflare
                if (
                    title.includes('just a moment')
                    || title.includes('attention required')
                    || title.includes('checking')
                ) {
                    return false;
                }

                return true;
            }
            """,
            timeout=timeout
        )
    except Exception:
        pass

    # انتظار إضافي للتأكد
    page.wait_for_timeout(3000)
