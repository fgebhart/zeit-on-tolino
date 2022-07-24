from pathlib import Path

from zeit_on_tolino import zeit

ZEIT_E_PAPER_URL = "https://epaper.zeit.de/abo/diezeit/"


def test__login(webdriver) -> None:
    url = zeit._login(webdriver)
    assert url == ZEIT_E_PAPER_URL


def test_download_e_paper(webdriver, tmp_path) -> None:
    e_paper_name = zeit.download_e_paper(webdriver)
    assert isinstance(e_paper_name, str)

    e_paper_path = Path(tmp_path) / e_paper_name
    assert e_paper_path.is_file()
    assert e_paper_path.suffix == ".epub"
