import logging
from pathlib import Path

from zeit_on_tolino import web, zeit

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    log.info("logging into ZEIT...")
    webdriver = web.get_webdriver()

    log.info("downloading most recent ZEIT e-paper...")
    e_paper_name = zeit.download_e_paper(webdriver)
    e_paper_path = Path(web.DOWNLOAD_PATH) / e_paper_name
    assert e_paper_path.is_file()
    log.info(f"finished download. Find e-paper at: {e_paper_path}")

    log.info("upload ZEIT e-paper...")

    webdriver.quit()
    log.info("done.")
