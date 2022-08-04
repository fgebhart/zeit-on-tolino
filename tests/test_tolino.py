import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from zeit_on_tolino import tolino


def test__login(webdriver) -> None:
    tolino._login(webdriver)
    assert "Angemeldet" in webdriver.page_source


def _delete_last_uploaded_epub(webdriver) -> None:
    # refresh page to ensure menu is closed for further interaction with the page
    webdriver.refresh()
    time.sleep(3)

    # wait for overlay object to be invisible
    WebDriverWait(webdriver, 10).until(EC.invisibility_of_element_located((By.ID, "splash-screen")))
    # note, the index=0 indicates that the most recently uploaded epub should be deleted as it is listed first
    index = 0
    epub_menu = WebDriverWait(webdriver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f'div[data-test-id="library-myBooks-titles-list-{index}-contextMenu"]')
        )
    )
    epub_menu.click()
    time.sleep(2)

    # click on delete
    for span in webdriver.find_elements(By.TAG_NAME, "span"):
        if span.text == "Löschen":
            span.click()
            break
    time.sleep(2)

    # confirm delete by clicking on 'ok'
    for span in webdriver.find_elements(By.TAG_NAME, "span"):
        if span.text == "OK":
            span.click()
            break
    time.sleep(2)


def test_upload_epub(webdriver, test_epub_path, test_epub_title) -> None:
    # verify test epub gets uploaded
    tolino.upload_e_paper(webdriver, test_epub_path)
    assert test_epub_title in webdriver.page_source

    # cleanup uploaded test epub
    _delete_last_uploaded_epub(webdriver)
    assert test_epub_title not in webdriver.page_source
