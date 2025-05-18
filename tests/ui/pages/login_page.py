from playwright.sync_api import Page, expect
from .base_page import BasePage

class LoginPage(BasePage):

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

        # === Locators ===
        self.email_in = 'input[type="email"]'
        self.password_in = 'input[type="password"]'
        self.login_btn = 'button[type="submit"]'
        self.register_btn = 'text=Register'
        self.form_header = 'h2:text("Login")'

    # === Actions ===
    def open(self):
        self.goto("/login")

    def fill_email(self, email: str):
        self.type_text(self.email_in, email)

    def fill_password(self, password: str):
        self.type_text(self.password_in, password)

    def click_login_btn(self):
        self.click(self.login_btn)

    def click_register_btn(self):
        self.click(self.register_btn)

    def login(self, email: str, password: str):
        self.fill_email(email)
        self.fill_password(password)
        self.click_login_btn()

    def navigate_to_register_page(self):
        self.click_register_btn()

    # === Expectations ===
    def expect_login_form_visible(self):
        expect(self.page.locator(self.form_header)).to_have_text("Login")
