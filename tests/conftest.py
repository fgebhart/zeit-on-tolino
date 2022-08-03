from pathlib import Path

import pytest

from zeit_on_tolino import web


@pytest.fixture
def webdriver(tmp_path):
    webdriver = web.get_webdriver(download_path=tmp_path)
    yield webdriver
    webdriver.quit()


@pytest.fixture
def test_epub_path():
    test_path = Path(__file__).parent
    yield test_path / "epub" / "around-the-world-in-28-languages.epub"


@pytest.fixture
def test_epub_title():
    yield "Around the World in 28 Languages"
