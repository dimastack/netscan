import pytest

from conftest import UI_TEST_URL, UI_USER_CREDENTIALS
from ui.pages.login_page import LoginPage


@pytest.mark.ui
def test_user_login(page):
    login_page = LoginPage(page, UI_TEST_URL)
    login_page.open()
    email = UI_USER_CREDENTIALS["email"]
    password = UI_USER_CREDENTIALS["password"]
    login_page.login(email, password)
    assert login_page.get_text("span.user-email") == email
    login_page.wait_for_url("/dashboard")
