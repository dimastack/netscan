import pytest

from conftest import UI_TEST_URL, UI_USER_CREDENTIALS
from ui.pages.login_page import LoginPage
from ui.pages.dashboard_page import DashboardPage


@pytest.mark.ui
def test_user_login(page):
    login_page = LoginPage(page, UI_TEST_URL)
    login_page.open()
    email = UI_USER_CREDENTIALS["email"]
    password = UI_USER_CREDENTIALS["password"]
    login_page.login(email, password)

    dashboard_page = DashboardPage(page, UI_TEST_URL)
    dashboard_page.wait_for_url("/dashboard")
    assert dashboard_page.get_logged_in_email() == email
