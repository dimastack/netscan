import pytest
from faker import Faker

from conftest import UI_TEST_URL
from ui.pages.login_page import LoginPage
from ui.pages.register_page import RegisterPage


@pytest.mark.ui
def test_user_successfully_registered(page):
    login_page = LoginPage(page, UI_TEST_URL)
    login_page.open()
    login_page.navigate_to_register_page()

    register_page = RegisterPage(page, UI_TEST_URL)
    assert register_page.get_text(register_page.form_header) == 'Register'

    fake = Faker()
    username = fake.user_name()
    email = fake.email()
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

    register_page.register(username, email, password)
    register_page.wait_for_url("/login")
    assert login_page.get_text(login_page.form_header) == 'Login'

    login_page.login(email, password)
    login_page.wait_for_url("/dashboard")
    assert login_page.get_text("span.user-email") == email
