import pytest

from zeit_on_tolino import web


@pytest.fixture
def webdriver(tmp_path):
    # download_path = tmp_path / "download"
    webdriver = web.get_webdriver(download_path=tmp_path)
    yield webdriver
    webdriver.quit()
