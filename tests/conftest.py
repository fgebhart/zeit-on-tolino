import pytest

from zeit_on_tolino import web


@pytest.fixture
def webdriver(tmp_path):
    webdriver = web.get_webdriver(download_path=tmp_path)
    yield webdriver
    webdriver.quit()
