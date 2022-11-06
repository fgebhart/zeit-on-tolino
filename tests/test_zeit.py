import os
from pathlib import Path

import pytest

from zeit_on_tolino import zeit
from zeit_on_tolino.env_vars import EnvVars, MissingEnvironmentVariable

ZEIT_E_PAPER_URL = "https://epaper.zeit.de/abo/diezeit"


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
    if EnvVars.ZEIT_PREMIUM_USER in os.environ and EnvVars.ZEIT_PREMIUM_PASSWORD in os.environ:
        del os.environ[EnvVars.ZEIT_PREMIUM_USER]
        del os.environ[EnvVars.ZEIT_PREMIUM_PASSWORD]

    # verify meaningful error is raised
    with pytest.raises(
        MissingEnvironmentVariable,
        match="Ensure to export your ZEIT username and password as environment variables",
    ):
        zeit.download_e_paper(webdriver)


def test_wrong_credentials(webdriver) -> None:
    # set wrong credentials
    os.environ[EnvVars.ZEIT_PREMIUM_USER] = "foo"
    os.environ[EnvVars.ZEIT_PREMIUM_PASSWORD] = "baa"

    # verify error is raised
    with pytest.raises(RuntimeError, match="Failed to login, check your login credentials."):
        zeit.download_e_paper(webdriver)
