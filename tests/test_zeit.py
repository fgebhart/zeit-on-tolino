import os
from pathlib import Path

import pytest

from zeit_on_tolino import zeit

ZEIT_E_PAPER_URL = "https://epaper.zeit.de/abo/diezeit/"


def test__login(webdriver) -> None:
    zeit._login(webdriver)
    assert webdriver.current_url == ZEIT_E_PAPER_URL


def test_download_e_paper(webdriver, tmp_path) -> None:
    e_paper_name = zeit.download_e_paper(webdriver)
    assert isinstance(e_paper_name, str)

    e_paper_path = Path(tmp_path) / e_paper_name
    assert e_paper_path.is_file()
    assert e_paper_path.suffix == ".epub"


def test_no_credentials(webdriver) -> None:
    # delete existing env vars
    if zeit.ENV_VAR_ZEIT_USER in os.environ and zeit.ENV_VAR_ZEIT_PW in os.environ:
        del os.environ[zeit.ENV_VAR_ZEIT_USER]
        del os.environ[zeit.ENV_VAR_ZEIT_PW]

    # verify meaningful error is raised
    with pytest.raises(KeyError, match="Ensure to export your ZEIT username and password as environment variables"):
        zeit.download_e_paper(webdriver)


def test_wrong_credentials(webdriver) -> None:
    # set wrong credentials
    os.environ[zeit.ENV_VAR_ZEIT_USER] = "foo"
    os.environ[zeit.ENV_VAR_ZEIT_PW] = "baa"

    # verify error is raised
    with pytest.raises(RuntimeError, match="Failed to login, check your login credentials."):
        zeit.download_e_paper(webdriver)
