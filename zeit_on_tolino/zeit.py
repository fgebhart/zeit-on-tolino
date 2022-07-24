from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

ZEIT_PREMIUM_URL = "https://premium.zeit.de/"
ZEIT_DATE_FORMAT = "%d.%m.%Y"


def _login(webdriver: WebDriver) -> str:
    webdriver.get(ZEIT_PREMIUM_URL)

    btn = webdriver.find_element(By.CLASS_NAME, "nav__login-link")
    btn.click()
    assert "anmelden" in webdriver.current_url, webdriver.current_url

    # username = webdriver.find_element(By.ID, "login_email")
    # password = webdriver.find_element(By.ID, "login_pass")
    # username.send_keys(ZEIT_PREMIUM_USER)
    # password.send_keys(ZEIT_PREMIUM_PASSWORD)
    btn = webdriver.find_element(By.CLASS_NAME, "submit-button.log")
    btn.click()

    return webdriver.current_url


def download_e_paper(webdriver: WebDriver) -> str:
    e_paper_url = _login(webdriver)
    webdriver.get(e_paper_url)

    for link in webdriver.find_elements(By.TAG_NAME, "a"):
        if link.text == "ZUR AKTUELLEN AUSGABE":
            link.click()
            break

    for link in webdriver.find_elements(By.TAG_NAME, "a"):
        if link.text == "EPUB FÜR E-READER LADEN":
            file_name = link.get_attribute("href").split("/")[-1]
            link.click()
            break

    return file_name
