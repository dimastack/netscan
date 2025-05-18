from playwright.sync_api import Page, expect

class BasePage:

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def goto(self, path: str = ""):
        """Navigate to a full path or relative route."""
        url = path if path.startswith("http") else f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        self.page.goto(url)

    def get_title(self):
        """Get the current page title."""
        return self.page.title()

    def wait_for_url(self, path: str, timeout: int = 5000):
        """Wait until the current URL matches the given path."""
        expected_url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        self.page.wait_for_url(expected_url, timeout=timeout)

    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        return self.page.locator(selector).is_visible()

    def click(self, selector: str):
        """Click on an element."""
        self.page.locator(selector).click()

    def type_text(self, selector: str, text: str):
        """Fill input field."""
        self.page.locator(selector).fill(text)

    def get_text(self, selector: str) -> str:
        """Get text content of an element."""
        return self.page.locator(selector).inner_text()

    def expect_url_contains(self, path_part: str):
        """Assert URL contains a specific part."""
        expect(self.page).to_have_url(f".*{path_part}.*")
