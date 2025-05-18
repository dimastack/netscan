from playwright.sync_api import Page, expect
from .base_page import BasePage

class RegisterPage(BasePage):

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

        # === Locators ===
        self.username_in = 'input[placeholder="Enter your username"]'
        self.email_in = 'input[placeholder="Enter your email"]'
        self.password_in = 'input[placeholder="Enter your password"]'
        self.register_btn = 'button[type="submit"]'
        self.form_header = 'h2:text("Register")'

    # === Actions ===
    def open(self):
        self.goto("/register")

    def fill_username(self, username: str):
        self.type_text(self.username_in, username)

    def fill_email(self, email: str):
        self.type_text(self.email_in, email)

    def fill_password(self, password: str):
        self.type_text(self.password_in, password)

    def fill_form(self, username: str, email: str, password: str):
        self.fill_username(username)
        self.fill_email(email)
        self.fill_password(password)

    def submit(self):
        self.click(self.register_btn)

    def register(self, username: str, email: str, password: str):
        self.fill_form(username, email, password)
        self.submit()

    # === Expectations ===
    def expect_register_form_visible(self):
        expect(self.page.locator("h2")).to_have_text("Register")
