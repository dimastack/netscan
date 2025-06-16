import os

def get_options(config):
    return {
        "API_TEST_URL": config.getoption("--api-url"),
        "UI_TEST_URL": config.getoption("--ui-url"),
        "BROWSER": config.getoption("--browser").lower(),
        "HEADLESS": config.getoption("--headless"),
    }

def add_options(parser):
    parser.addoption(
        "--api-url",
        action="store",
        default=os.getenv("BACKEND_URL", "http://localhost:5001/api/v1"),
        help="Base URL for the API"
    )
    parser.addoption(
        "--ui-url",
        action="store",
        default=os.getenv("UI_URL", "http://localhost:5173"),
        help="Base Frontend URL"
    )
    parser.addoption(
        "--browser",
        action="store",
        default=os.getenv("BROWSER", "chromium"),
        help="Browser to use: chromium, firefox, or webkit"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )
