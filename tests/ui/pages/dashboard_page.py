from playwright.sync_api import Page
from ui.pages.base_page import BasePage


class DashboardPage(BasePage):

    VALID_FEATURES = {
        # DNS section
        "DNS Lookup",
        "Reverse DNS",
        "WHOIS",
        # SCAN section
        "Banner Grabbing",
        "OS Fingerprint",
        "Ping",
        "TCP SYN Scan",
        "TCP Connect Scan",
        "UDP Scan",
        "Port Scan",
        "Traceroute",
        # UTILS section
        "Headers",
        "Latency",
        "Resolve",
        "Reverse Lookup",
        # WEB section
        "HTTP Check",
        "SSL Check",
    }

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.menu_btn = ".menu-toggle-btn"
        self.section_title = ".section-title"
        self.menu_label = ".menu-label"
        self.active_menu_item = ".sidebar .menu-item.active"
        self.user_email = "span.user-email"
        self.logout_button = "button.primary-button:has-text('Logout')"

    # --- Navigation ---
    def open(self):
        self.goto("/dashboard")

    # --- Actions ---
    def toggle_menu(self):
        """Toggle the sidebar menu."""
        self.click(self.menu_btn)

    def click_menu_item(self, item_name: str):
        """Click on a menu item by its name."""
        locator = f"{self.menu_label}:has-text('{item_name}')"
        self.click(locator)

    def toggle(self, feature_name: str):
        """Click the toggle button for a given feature."""
        if feature_name not in self.VALID_FEATURES:
            raise ValueError(
                f"'{feature_name}' is not a valid feature toggle. "
                f"Expected one of: {', '.join(sorted(self.VALID_FEATURES))}"
            )
        locator = f"button.dropdown-toggle:has-text('{feature_name}')"
        self.click(locator)

    def is_toggle_visible(self, feature_name: str) -> bool:
        """Check if the toggle for a given feature is visible."""
        if feature_name not in self.VALID_FEATURES:
            raise ValueError(
                f"'{feature_name}' is not a valid feature toggle. "
                f"Expected one of: {', '.join(sorted(self.VALID_FEATURES))}"
            )
        locator = f"button.dropdown-toggle:has-text('{feature_name}')"
        return self.is_visible(locator)
    
    def logout(self):
        self.click(self.logout_button)

    # --- Assertions / Checks ---
    def get_logged_in_email(self) -> str:
        return self.get_text(self.user_email)

    def is_user_email_visible(self) -> bool:
        return self.is_visible(self.user_email)

    def get_active_menu_icon_text(self) -> str:
        return self.get_text(f"{self.active_menu_item} .menu-icon")

    def get_section_title(self) -> str:
        return self.get_text(self.section_title)
