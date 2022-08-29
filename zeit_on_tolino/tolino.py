import logging
import os
import time
from pathlib import Path
from typing import Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from zeit_on_tolino import MissingEnvironmentVariable, epub
from zeit_on_tolino.tolino_partner import PartnerDetails
from zeit_on_tolino.web import Delay

ENV_VAR_TOLINO_USER = "TOLINO_USER"
ENV_VAR_TOLINO_PW = "TOLINO_PASSWORD"
ENV_VAR_TOLINO_PARTNER_SHOP = "TOLINO_PARTNER_SHOP"

TOLINO_CLOUD_LOGIN_URL = "https://webreader.mytolino.com/"
TOLINO_COUNTRY_TO_SELECT = "Deutschland"  # TODO make country a partner shop detail depending on selected partner shop

BUTTON_PLEASE_SELECT_YOUR_COUNTRY = "Bitte wähle Dein Land aus"
BUTTON_LOGIN = "Anmelden"
BUTTON_UPLOAD = "Hochladen"


log = logging.getLogger(__name__)


def _get_credentials() -> Tuple[str, str, str]:
    try:
        username = os.environ[ENV_VAR_TOLINO_USER]
        password = os.environ[ENV_VAR_TOLINO_PW]
        partner_shop = os.environ[ENV_VAR_TOLINO_PARTNER_SHOP]
        return username, password, partner_shop
    except KeyError:
        raise MissingEnvironmentVariable(
            f"Ensure to export your tolino username, password and partner shop as environment variables "
            f"'{ENV_VAR_TOLINO_USER}', '{ENV_VAR_TOLINO_PW}' and '{ENV_VAR_TOLINO_PARTNER_SHOP}'. "
            f"For Github Actions, use repository secrets."
        )


def _login(webdriver: WebDriver) -> None:
    username, password, partner_shop = _get_credentials()
    pd = getattr(PartnerDetails, partner_shop.lower()).value
    webdriver.get(TOLINO_CLOUD_LOGIN_URL)

    # select country
    WebDriverWait(webdriver, Delay.medium).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="ftu-countrySelection-countryList"]'))
    )
    WebDriverWait(webdriver, Delay.medium).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="ftu-country-de-DE"]'))
    )
    time.sleep(Delay.small)
    for div in webdriver.find_elements(By.TAG_NAME, "div"):
        if div.text == TOLINO_COUNTRY_TO_SELECT:
            div.click()
            break
    else:
        raise RuntimeError(f"Could not select desired country '{TOLINO_COUNTRY_TO_SELECT}'.")

    # select partner shop
    WebDriverWait(webdriver, Delay.medium).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="ftu-resellerSelection-resellerList"]'))
    )
    for div in webdriver.find_elements(By.TAG_NAME, "div"):
        if pd.shop_image_keyword in div.get_attribute("style"):
            div.click()
            break
    else:
        raise RuntimeError(f"Could not select desired partner shop '{pd.shop_image_keyword}'.")

    # click on login button
    WebDriverWait(webdriver, Delay.medium).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="library-selection-headerBar"]'))
    )
    for span in webdriver.find_elements(By.TAG_NAME, "span"):
        if span.text == BUTTON_LOGIN:
            span.click()
            break
    else:
        raise RuntimeError("Could not find login button.")

    # login with partner shop credentials
    WebDriverWait(webdriver, Delay.medium).until(EC.presence_of_element_located((pd.user.by, pd.user.value)))
    username_field = webdriver.find_element(pd.user.by, pd.user.value)
    username_field.send_keys(username)
    password_field = webdriver.find_element(pd.password.by, pd.password.value)
    password_field.send_keys(password)

    btn = webdriver.find_element(pd.login_button.by, pd.login_button.value)
    btn.click()
    WebDriverWait(webdriver, Delay.large).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-test-id="library-drawer-labelLoggedIn"]'))
    )


def upload_e_paper(webdriver: WebDriver, file_path: Path) -> None:
    log.info("logging into tolino cloud...")
    _login(webdriver)

    # click on 'my books'
    my_books_button_css = 'span[data-test-id="library-drawer-MyBooks"]'
    WebDriverWait(webdriver, Delay.small).until(EC.presence_of_element_located((By.CSS_SELECTOR, my_books_button_css)))
    my_books_button = webdriver.find_element(By.CSS_SELECTOR, my_books_button_css)
    my_books_button.click()

    # click on vertical ellipsis to get to drop down menu
    menu_css = 'svg[data-test-id="library-headerBar-overflowMenu-button"]'
    WebDriverWait(webdriver, Delay.medium).until(EC.presence_of_element_located((By.CSS_SELECTOR, menu_css)))
    menu = webdriver.find_element(By.CSS_SELECTOR, menu_css)
    menu.click()

    # upload file
    WebDriverWait(webdriver, Delay.small).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test-id="library-headerBar-popup-menu"]'))
    )
    upload = webdriver.find_element(By.XPATH, "//input[@type='file']")
    upload.send_keys(str(file_path))

    # wait for upload status field to appear
    log.info("waiting for upload status bar to appear...")
    WebDriverWait(webdriver, Delay.medium).until(EC.presence_of_element_located((By.CLASS_NAME, "_ymr9b9")))
    log.info("upload status bar appeared.")
    # wait for upload status field to disappear
    log.info("waiting for upload status bar to disappear...")
    upload_status_bar = webdriver.find_element(By.CLASS_NAME, "_ymr9b9")
    WebDriverWait(webdriver, Delay.xlarge).until(EC.staleness_of(upload_status_bar))
    log.info("upload status bar disappeared.")
    time.sleep(Delay.medium)

    webdriver.refresh()
    log.info("waiting for book titles to be present...")
    WebDriverWait(webdriver, Delay.medium).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[data-test-id="library-myBooks-titles-list-0-title"]'))
    )
    log.info("book titles are present.")

    epub_title = epub.get_epub_info(file_path)["title"]
    assert epub_title in webdriver.page_source, f"Title '{epub_title}' not found in page source!"
    log.info(f"book title '{epub_title}' is present.")
