import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from zeit_on_tolino import tolino
from zeit_on_tolino.env_vars import EnvVars
from zeit_on_tolino.web import Delay


def test__login(webdriver) -> None:
    tolino._login(webdriver)
    # wait until logged in
    WebDriverWait(webdriver, Delay.large).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-test-id="library-drawer-labelLoggedIn"]'))
    )
    assert "Angemeldet" in webdriver.page_source


def _delete_last_uploaded_epub(webdriver: WebDriver) -> None:
    # refresh page to ensure menu is closed for further interaction with the page
    webdriver.refresh()
    time.sleep(Delay.small)

    # wait for overlay object to be invisible
    WebDriverWait(webdriver, Delay.medium).until(EC.invisibility_of_element_located((By.ID, "splash-screen")))
    # note, the index=0 indicates that the most recently uploaded epub should be deleted as it is listed first
    index = 0
    epub_menu = WebDriverWait(webdriver, Delay.large).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f'div[data-test-id="library-myBooks-titles-list-{index}-contextMenu"]')
        )
    )
    epub_menu.click()
    time.sleep(Delay.small)

    # click on delete
    for span in webdriver.find_elements(By.TAG_NAME, "span"):
        if span.text == "Löschen":
            span.click()
            break
    time.sleep(Delay.small)

    # confirm delete by clicking on 'ok'
    for span in webdriver.find_elements(By.TAG_NAME, "span"):
        if span.text == "OK":
            span.click()
            break
    time.sleep(Delay.small)


def test_upload_epub(webdriver, test_epub_path, test_epub_title, caplog) -> None:
    caplog.set_level(logging.INFO)

    # verify test epub gets uploaded
    tolino.login_and_upload(webdriver, test_epub_path, test_epub_title)
    assert test_epub_title in webdriver.page_source

    # try uploading again to verify it will simply skip uploading
    tolino._upload(webdriver, test_epub_path, test_epub_title)
    assert f"The title '{test_epub_title}' is already present in tolino cloud. Skipping upload." in caplog.text

    # cleanup uploaded test epub
    _delete_last_uploaded_epub(webdriver)
    assert test_epub_title not in webdriver.page_source
