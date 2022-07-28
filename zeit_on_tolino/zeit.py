import os

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

ENV_VAR_ZEIT_USER = "ZEIT_PREMIUM_USER"
ENV_VAR_ZEIT_PW = "ZEIT_PREMIUM_PASSWORD"
ZEIT_PREMIUM_URL = "https://premium.zeit.de/"
ZEIT_DATE_FORMAT = "%d.%m.%Y"
BUTTON_TEXT_TO_RECENT_EDITION = "ZUR AKTUELLEN AUSGABE"
BUTTON_TEXT_DOWNLOAD_EPUB = "EPUB FÜR E-READER LADEN"


def _login(webdriver: WebDriver) -> str:
    username = os.environ[ENV_VAR_ZEIT_USER]
    password = os.environ[ENV_VAR_ZEIT_PW]

    webdriver.get(ZEIT_PREMIUM_URL)

    btn = webdriver.find_element(By.CLASS_NAME, "nav__login-link")
    btn.click()
    assert "anmelden" in webdriver.current_url, webdriver.current_url

    username_field = webdriver.find_element(By.ID, "login_email")
    username_field.send_keys(username)
    password_field = webdriver.find_element(By.ID, "login_pass")
    password_field.send_keys(password)

    btn = webdriver.find_element(By.CLASS_NAME, "submit-button.log")
    btn.click()

    if "anmelden" in webdriver.current_url:
        raise RuntimeError("Failed to login, check your login credentials.")

    return webdriver.current_url


def download_e_paper(webdriver: WebDriver) -> str:
    e_paper_url = _login(webdriver)
    webdriver.get(e_paper_url)

    for link in webdriver.find_elements(By.TAG_NAME, "a"):
        if link.text == BUTTON_TEXT_TO_RECENT_EDITION:
            link.click()
            break

    file_name = None
    for link in webdriver.find_elements(By.TAG_NAME, "a"):
        if link.text == BUTTON_TEXT_DOWNLOAD_EPUB:
            file_name = link.get_attribute("href").split("/")[-1]
            link.click()
            break

    if not file_name:
        raise RuntimeError("Could not locate download button, check your login credentials.")

    return file_name
