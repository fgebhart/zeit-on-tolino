import os
import time
from pathlib import Path
from typing import Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from zeit_on_tolino.tolino_partner import PartnerDetails

ENV_VAR_TOLINO_USER = "TOLINO_USER"
ENV_VAR_TOLINO_PW = "TOLINO_PASSWORD"
ENV_VAR_TOLINO_PARTNER_SHOP = "TOLINO_PARTNER_SHOP"

TOLINO_CLOUD_LOGIN_URL = "https://webreader.mytolino.com/"
TOLINO_COUNTRY_TO_SELECT = "Deutschland"  # TODO make country a partner shop detail depending on selected partner shop

BUTTON_PLEASE_SELECT_YOUR_COUNTRY = "Bitte wähle Dein Land aus"
BUTTON_LOGIN = "Anmelden"
BUTTON_MY_BOOKS = "Meine Bücher"
BUTTON_UPLOAD = "Hochladen"


def _get_credentials() -> Tuple[str, str, str]:
    try:
        username = os.environ[ENV_VAR_TOLINO_USER]
        password = os.environ[ENV_VAR_TOLINO_PW]
        partner_shop = os.environ[ENV_VAR_TOLINO_PARTNER_SHOP]
        return username, password, partner_shop
    except KeyError:
        raise KeyError(
            f"Ensure to export your tolino username, password and partner shop as environment variables "
            f"'{ENV_VAR_TOLINO_USER}', '{ENV_VAR_TOLINO_PW}' and '{ENV_VAR_TOLINO_PARTNER_SHOP}'. "
            f"For Github Actions, use repository secrets."
        )


def _login(webdriver: WebDriver) -> str:
    username, password, partner_shop = _get_credentials()
    pd = getattr(PartnerDetails, partner_shop.lower()).value
    webdriver.get(TOLINO_CLOUD_LOGIN_URL)

    # select country
    time.sleep(3)
    for div in webdriver.find_elements(By.TAG_NAME, "div"):
        if div.text == TOLINO_COUNTRY_TO_SELECT:
            div.click()
            break

    # select partner shop
    time.sleep(3)
    for div in webdriver.find_elements(By.TAG_NAME, "div"):
        if pd.shop_image_keyword in div.get_attribute("style"):
            div.click()
            break

    # click on login button
    time.sleep(3)
    for span in webdriver.find_elements(By.TAG_NAME, "span"):
        if span.text == BUTTON_LOGIN:
            span.click()
            break

    # login with partner shop credentials
    time.sleep(3)
    WebDriverWait(webdriver, 3).until(EC.presence_of_element_located((pd.user.by, pd.user.value)))
    username_field = webdriver.find_element(pd.user.by, pd.user.value)
    username_field.send_keys(username)

    password_field = webdriver.find_element(pd.password.by, pd.password.value)
    password_field.send_keys(password)
    btn = webdriver.find_element(pd.login_button.by, pd.login_button.value)
    btn.click()

    time.sleep(3)
    return webdriver.current_url


def upload_e_paper(webdriver: WebDriver, file_path: Path) -> str:
    tolino_cloud_url = _login(webdriver)
    webdriver.get(tolino_cloud_url)

    # click on 'my books'
    time.sleep(5)
    for span in webdriver.find_elements(By.TAG_NAME, "span"):
        if span.text == BUTTON_MY_BOOKS:
            span.click()
            break

    # click on vertical ellipsis to get to drop down menu
    time.sleep(3)
    menu = webdriver.find_element(By.CSS_SELECTOR, "._y4tlgh")
    menu.click()

    # upload file
    time.sleep(3)
    upload = webdriver.find_element(By.XPATH, "//input[@type='file']")
    upload.send_keys(str(file_path))

    # wait until upload has finished
    # TODO replace by proper wait functions (1. wait for download window to show up and wait for it to disappear again)
    time.sleep(15)

    # refresh page to ensure menu is closed for further interaction with the page
    webdriver.refresh()
    time.sleep(3)
