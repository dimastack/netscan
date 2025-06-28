import pytest
import requests

from playwright.sync_api import sync_playwright

from config import get_options
from conftest import UI_USER_CREDENTIALS, HEADLESS

@pytest.fixture(scope="session")
def browser_context(request):
    opts = get_options(request.config)
    browser_name = opts["BROWSER"]

    with sync_playwright() as p:
        browser = {
            "chromium": p.chromium,
            "firefox": p.firefox,
            "webkit": p.webkit,
        }.get(browser_name)

        if not browser:
            raise ValueError(f"Unsupported browser: {browser_name}")

        instance = browser.launch(headless=HEADLESS)
        context = instance.new_context()
        yield context
        context.close()
        instance.close()

@pytest.fixture(scope="session")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session", autouse=True)
def register_ui_user(request):
    opts = get_options(request.config)
    try:
        requests.post(
            f"{opts['API_TEST_URL']}/auth/register",
            json=UI_USER_CREDENTIALS,
            timeout=5
        )
    except requests.RequestException:
        pass
