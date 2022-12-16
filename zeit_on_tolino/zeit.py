import os
import time
from typing import Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from zeit_on_tolino.env_vars import EnvVars, MissingEnvironmentVariable
from zeit_on_tolino.web import Delay

ZEIT_LOGIN_URL = "https://premium.zeit.de/"
ZEIT_DATE_FORMAT = "%d.%m.%Y"

BUTTON_TEXT_TO_RECENT_EDITION = "ZUR AKTUELLEN AUSGABE"
BUTTON_TEXT_DOWNLOAD_EPUB = "EPUB FÜR E-READER LADEN"
BUTTON_TEXT_EPUB_DOWNLOAD_IS_PENDING = "EPUB FOLGT IN KÜRZE"


def _get_credentials() -> Tuple[str, str]:
    try:
        username = os.environ[EnvVars.ZEIT_PREMIUM_USER]
        password = os.environ[EnvVars.ZEIT_PREMIUM_PASSWORD]
        return username, password
    except KeyError:
        raise MissingEnvironmentVariable(
            f"Ensure to export your ZEIT username and password as environment variables "
            f"'{EnvVars.ZEIT_PREMIUM_USER}' and '{EnvVars.ZEIT_PREMIUM_PASSWORD}'. For "
            "Github Actions, use repository secrets."
        )


def _login(webdriver: WebDriver) -> None:
    username, password = _get_credentials()
    webdriver.get(ZEIT_LOGIN_URL)

    WebDriverWait(webdriver, Delay.medium).until(EC.presence_of_element_located((By.CLASS_NAME, "nav__login-link")))
    btn = webdriver.find_element(By.CLASS_NAME, "nav__login-link")
    btn.click()
    assert "anmelden" in webdriver.current_url, webdriver.current_url

    username_field = webdriver.find_element(By.ID, "login_email")
    username_field.send_keys(username)
    password_field = webdriver.find_element(By.ID, "login_pass")
    password_field.send_keys(password)

    btn = webdriver.find_element(By.CLASS_NAME, "submit-button.log")
    btn.click()
    time.sleep(Delay.small)

    if "anmelden" in webdriver.current_url:
        raise RuntimeError("Failed to login, check your login credentials.")

    WebDriverWait(webdriver, Delay.medium).until(EC.presence_of_element_located((By.CLASS_NAME, "page-section-header")))


def download_e_paper(webdriver: WebDriver) -> str:
    _login(webdriver)

    time.sleep(Delay.small)
    for link in webdriver.find_elements(By.TAG_NAME, "a"):
        if link.text == BUTTON_TEXT_TO_RECENT_EDITION:
            link.click()
            break

    if BUTTON_TEXT_EPUB_DOWNLOAD_IS_PENDING in webdriver.page_source:
        raise RuntimeError("New ZEIT release is available, however, EPUB version is not. Retry again later.")

    time.sleep(Delay.small)
    file_name = None
    for link in webdriver.find_elements(By.TAG_NAME, "a"):
        if link.text == BUTTON_TEXT_DOWNLOAD_EPUB:
            file_name = link.get_attribute("href").split("/")[-1]
            link.click()
            break

    if not file_name:
        raise RuntimeError("Could not locate download button, check your login credentials.")

    return file_name
