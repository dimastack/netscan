import pytest

from conftest import UI_TEST_URL, UI_USER_CREDENTIALS
from ui.pages.login_page import LoginPage
from ui.pages.dashboard_page import DashboardPage


@pytest.mark.ui
def test_dashboard(page):
    login_page = LoginPage(page, UI_TEST_URL)
    login_page.open()
    email = UI_USER_CREDENTIALS["email"]
    password = UI_USER_CREDENTIALS["password"]
    login_page.login(email, password)
    assert login_page.get_text("span.user-email") == email
    login_page.wait_for_url("/dashboard")

    dashboard_page = DashboardPage(page, UI_TEST_URL)
    assert dashboard_page.get_logged_in_email() == email
    assert dashboard_page.get_section_title() == 'DNS'

    assert dashboard_page.is_toggle_visible("DNS Lookup") == True
    assert dashboard_page.is_toggle_visible("Reverse DNS") == True
    assert dashboard_page.is_toggle_visible("WHOIS") == True

    dashboard_page.toggle("DNS Lookup")
    dashboard_page.toggle("Reverse DNS")
    dashboard_page.toggle("WHOIS")

    dashboard_page.toggle_menu()

    dashboard_page.click_menu_item("Scan")
    assert dashboard_page.get_section_title() == 'SCAN'

    assert dashboard_page.is_toggle_visible("Banner Grabbing") == True
    assert dashboard_page.is_toggle_visible("OS Fingerprint") == True
    assert dashboard_page.is_toggle_visible("Ping") == True
    assert dashboard_page.is_toggle_visible("TCP SYN Scan") == True
    assert dashboard_page.is_toggle_visible("TCP Connect Scan") == True
    assert dashboard_page.is_toggle_visible("UDP Scan") == True
    assert dashboard_page.is_toggle_visible("Port Scan") == True
    assert dashboard_page.is_toggle_visible("Traceroute") == True

    dashboard_page.toggle("Banner Grabbing")
    dashboard_page.toggle("OS Fingerprint")
    dashboard_page.toggle("Ping")
    dashboard_page.toggle("TCP SYN Scan")
    dashboard_page.toggle("TCP Connect Scan")
    dashboard_page.toggle("UDP Scan")
    dashboard_page.toggle("Port Scan")
    dashboard_page.toggle("Traceroute")

    dashboard_page.click_menu_item("Utils")
    assert dashboard_page.get_section_title() == 'UTILS'

    assert dashboard_page.is_toggle_visible("Headers") == True
    assert dashboard_page.is_toggle_visible("Latency") == True
    assert dashboard_page.is_toggle_visible("Resolve") == True
    assert dashboard_page.is_toggle_visible("Reverse Lookup") == True

    dashboard_page.toggle("Headers")
    dashboard_page.toggle("Latency")
    dashboard_page.toggle("Resolve")
    dashboard_page.toggle("Reverse Lookup")

    dashboard_page.click_menu_item("Web")
    assert dashboard_page.get_section_title() == 'WEB'

    assert dashboard_page.is_toggle_visible("HTTP Check") == True
    assert dashboard_page.is_toggle_visible("SSL Check") == True

    dashboard_page.toggle("HTTP Check")
    dashboard_page.toggle("SSL Check")

    dashboard_page.logout()
    login_page.wait_for_url("/login")
    login_page.expect_login_form_visible()
